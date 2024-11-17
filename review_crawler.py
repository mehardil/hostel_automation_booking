"""review crawler"""
import os
import hashlib
import requests
import pandas as pd
from lxml import etree
from booking_selectors import review_selectors
# from custom_exception import NoDataError, NetworkError
import config
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk import capture_exception
from logs import LogManager


load_dotenv()

# Logs Confguration
log_manager = LogManager("booking_crawler")
log_manager.log("info", "Script initialized")
# Santry Configuration
sentry_config = {"DSN": os.environ["dsn"]}
sentry_sdk.init(
    dsn=sentry_config["DSN"],
    traces_sample_rate=1.0,
)


class BookingScraper:
    """Booking.com Scrapper Class"""

    def __init__(self, url, review_hash, total_reviews):
        self.flag = True
        self.total_reviews = total_reviews
        self.urls = url
        self.review_hash = review_hash
        self.selectors = review_selectors().__dict__
        self.headers = config.headers
        self.cookies = config.cookies

    def scrape(self):
        """Scrapper function"""
        for url in self.urls:
            batch_size = 10
            try:
                log_manager.log("info", f"Got this URL {url}")
                cc = url.split("/")[4]
                hotel_name = url.split("/")[5].split(".")[0]
            except UnboundLocalError as error:
                log_manager.log(
                    "error", f"Error parsing URL: {url}. Exception: {error}"
                )
                capture_exception(error)
            for offset in range(0, self.total_reviews, batch_size):
                if self.flag == False:
                    break
                params = {
                    "aid": "304142",
                    "label": "gen173nr-1FCAEoggI46AdIM1gEaLUBiAEBmAEJuAEXyAEM2AEB6AEB-AEMiAIBqAIDuALg2rauBsACAdICJDZlZDVhN2ZlLTk0YmItNDQ2YS05NGY2LWE0NzFjNWJiNTVmMdgCBuACAQ",
                    "sid": "da4bda249511a0264bb9e60631708902",
                    "cc1": str(cc),
                    "dist": "1",
                    "pagename": str(hotel_name),
                    "sort": "f_recent_desc",
                    "srpvid": "6be12cb2ea9e0058",
                    "type": "total",
                    "offset": str(offset),
                    "rows": "10",
                    "_": "1707978093291",
                }
                try:
                    response = requests.get(
                        "https://www.booking.com/reviewlist.en-gb.html",
                        params=params,
                        cookies=self.cookies,
                        headers=self.headers,
                        timeout=10,
                    )
                except requests.RequestException as error:
                    log_manager.log(
                        "error", f"Request error for URL: {url}. Exception: {error}"
                    )
                try:
                    if 400 <= response.status_code < 600:
                        # here we add message in santry
                        log_manager.log("error", f"Link not accessible for URL: {url}")
                        return False
                    self.data_parser(response.text)
                except UnboundLocalError as error:
                    log_manager.log(
                        "error", f"Error accessing api : Exception: {error}"
                    )
                    break
            log_manager.log("info", f"Scrapping completed for URL: {url}")

    def data_parser(self, website_content):
        """Parse website content and extract review data."""
        try:
            tree = etree.HTML(website_content)
            review_blocks = tree.xpath(self.selectors.get("review_block_xpath"))
            # total_reviews_data = tree.xpath(self.selectors.get("total_review_xpath"))
            # print(total_reviews_data,"here first check total number of review")
            # input("wait")
            if not review_blocks:
                log_manager.log("info", f"No review found OR XPath is not working")
                return
            for review_block in review_blocks:
                page_review_data = {
                    "reviewer_name": self.extract_reviewer_name(review_block),
                    "reviewer_country": self.extract_reviewer_country(review_block),
                    "room_type": self.extract_room_type(review_block),
                    "stay_duration": self.extract_stay_duration(review_block),
                    "stay_date": self.extract_stay_date(review_block),
                    "traveller_type": self.extract_traveller_type(review_block),
                    "review_date": self.extract_review_date(review_block),
                    "review_title": self.extract_review_title(review_block),
                    "review_rating": self.extract_review_rating(review_block),
                    "positive_review": self.extract_positive_review(review_block),
                    "negative_review": self.extract_negative_review(review_block),
                    "hotel_response": self.extract_hotel_response(review_block),
                    "review_photos": self.extract_review_photos(review_block),
                }
                page_review_data["review_hash"] = hashlib.md5(
                    str(page_review_data).encode()
                ).hexdigest()
                if self.review_hash == page_review_data["review_hash"]:
                    self.flag = False
                    break
                # Check if data already exists
                # if not self.check_existing_data(page_review_data):
                self.write_to_csv(page_review_data)
                # else:
                # print("Data already exists.")

        except etree.ParserError as e:
            print(f"Error parsing HTML: {e}")
            log_manager.log("error", "Error parsing etree HTML")

    def extract_reviewer_name(self, review_block):
        """Extract reviewer name"""
        reviewer_name_nodes = review_block.xpath(
            self.selectors.get("reviewer_name_xpath")
        )
        if not reviewer_name_nodes:
            capture_exception("Reviewer name XPath issue")
        return reviewer_name_nodes[0].strip() if reviewer_name_nodes else "None"

    def extract_reviewer_country(self, review_block):
        """Extract reviewer country"""
        reviewer_country_nodes = review_block.xpath(
            self.selectors.get("reviewer_country_xpath")
        )
        return reviewer_country_nodes[0].strip() if reviewer_country_nodes else "None"

    def extract_room_type(self, review_block):
        """Extract room type"""
        room_type_texts = review_block.xpath(self.selectors.get("room_type_xpath"))
        return "".join([text.strip() for text in room_type_texts if text.strip()])

    def extract_stay_duration(self, review_block):
        """Extract stay duration."""
        stay_duration_texts = review_block.xpath(
            self.selectors.get("stay_duration_xpath")
        )
        return " ".join(
            [
                f"{text.strip().split(' ')[0]} nights"
                for text in stay_duration_texts
                if text.strip()
            ]
        )

    def extract_stay_date(self, review_block):
        """Extract stay date."""
        stay_date_texts = review_block.xpath(self.selectors.get("stay_date_xpath"))
        return stay_date_texts[0].strip() if stay_date_texts else "None"

    def extract_traveller_type(self, review_block):
        """Extract traveller type."""
        traveller_type_texts = review_block.xpath(
            self.selectors.get("traveller_type_xpath")
        )
        return traveller_type_texts[0].strip() if traveller_type_texts else "None"

    def extract_review_date(self, review_block):
        """Extract review date"""
        review_date_texts = review_block.xpath(self.selectors.get("review_date_xpath"))
        review_date = review_date_texts[0].strip() if review_date_texts else "None"
        if "Reviewed:" in review_date:
            review_date = review_date.replace("Reviewed:", "")
        return review_date

    def extract_review_title(self, review_block):
        """Extract review title"""
        review_title_texts = review_block.xpath(
            self.selectors.get("review_title_xpath")
        )
        return review_title_texts[0].strip() if review_title_texts else "None"

    def extract_review_rating(self, review_block):
        """Extract review rating"""
        review_rating_nodes = review_block.xpath(
            self.selectors.get("review_rating_xpath")
        )
        return review_rating_nodes[0] if review_rating_nodes else "None"

    def extract_positive_review(self, review_block):
        """Extract positive review"""
        positive_review_text = review_block.xpath(
            self.selectors.get("positive_review_xpath")
        )
        return positive_review_text[0] if positive_review_text else "None"

    def extract_negative_review(self, review_block):
        """Extract negative review"""
        negative_review_text = review_block.xpath(
            self.selectors.get("negative_review_xpath")
        )
        return negative_review_text[0] if negative_review_text else "None"

    def extract_hotel_response(self, review_block):
        """Extract hotel response."""
        hotel_response_text = review_block.xpath(
            self.selectors.get("hotel_response_xpath")
        )
        return hotel_response_text[0] if hotel_response_text else "None"

    def extract_review_photos(self, review_block):
        """Extract review photos"""
        review_photos = review_block.xpath(self.selectors.get("review_photos_xpath"))
        return len(review_photos) if review_photos else "None"

    def write_to_csv(self, page_review_data):
        """Store dataset into CSV using pandas"""
        csv_file = "booking_testing_data.csv"
        try:
            # Convert review data to DataFrame
            df = pd.DataFrame([page_review_data])
            # If file exists, append to it, otherwise create new file
            mode = "a" if os.path.isfile(csv_file) else "w"
            # Write DataFrame to CSV
            df.to_csv(
                csv_file, mode=mode, index=False, header=not os.path.isfile(csv_file)
            )
        except PermissionError:
            print(f"Error: Permission denied to write to CSV file '{csv_file}'.")
            log_manager.log(
                "error", f"Error: Permission denied to write to CSV file: {csv_file}."
            )
        except UnicodeEncodeError as e:
            print(f"Error: Unicode encoding error while writing to CSV file: {e}.")
            log_manager.log(
                "error",
                f"Error: Unicode encoding error while writing to CSV file: {csv_file}",
            )


if __name__ == "__main__":
    # function that get url , total reviews from database
    urls = [
        "https://www.booking.com/hotel/us/park-lane-new-york.en-gb.html?aid=355028&sid=da4bda249511a0264bb9e60631708902&dest_id=20088325&dest_type=city&group_adults=2&group_children=0&hapos=7&hpos=7&keep_landing=1&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&srepoch=1653886966&srpvid=ad73237a01a2015b&type=total&ucfs=1&#tab-reviews"
    ]
    csv_file = "booking_testing_data.csv"
    if os.path.isfile(csv_file):
        df = pd.read_csv(csv_file)
        review_hash = df["review_hash"][0]
    else:
        review_hash = None
    scraper = BookingScraper(urls, review_hash, total_reviews=20)
    scraper.scrape()
