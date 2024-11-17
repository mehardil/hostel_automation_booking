"""Hotel Data Scrapper"""

import csv
import os
import hashlib
import requests
from lxml import etree
from booking_selectors import hotel_data_selectors


class HotelScraper:
    """Hotel data scraper class"""

    def __init__(self, url):
        self.urls = url
        self.selectors = hotel_data_selectors().__dict__

    def scrape(self):
        """Function to scrape the hotel data"""

        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
                if 400 <= response.status_code < 500:
                    print(f"Link not accessible: {url}")
                    continue
                self.data_parser(response.text)
            except requests.RequestException as e:
                print(f"Request error: {e}")

    def data_parser(self, website_content):
        """Function to parse the data"""
        try:
            tree = etree.HTML(website_content)
            hotel_name = tree.xpath(self.selectors.get("hotel_name_xpath"))[0]
            hotel_address = tree.xpath(self.selectors.get("hotel_address_xpath"))[
                0
            ].replace("\n", "")
            hotel_description = tree.xpath(
                self.selectors.get("hotel_description_xpath")
            )[0]
            hotel_rating = tree.xpath(self.selectors.get("hotel_rating_xpath"))[0]
            total_reviews = (
                tree.xpath(self.selectors.get("total_reviews_xpath"))[0]
                .replace("Guest reviews", "")
                .replace("(", "")
                .replace(")", "")
                .replace(",", "")
            )

            # Extract sub-categories and ratings
            sub_categories_text = tree.xpath(self.selectors.get("sub_categories_xpath"))
            sub_categories = [
                sub_category.strip()
                for sub_category in sub_categories_text
                if sub_category.strip()
            ]
            sub_categories_rating = tree.xpath(
                self.selectors.get("sub_categories_rating_xpath")
            )
            sub_categories_data = dict(zip(sub_categories, sub_categories_rating))
            popular_facilities = tree.xpath(
                self.selectors.get("popular_facilities_xpath")
            )
            hotel_surroundings = tree.xpath(
                self.selectors.get("hotel_surroundings_xpath")
            )
            hotel_surroundings_distance = tree.xpath(
                self.selectors.get("hotel_surroundings_distance_xpath")
            )
            hotel_surroundings_data = [
                f"{surrounding} - {distance}"
                for surrounding, distance in zip(
                    hotel_surroundings, hotel_surroundings_distance
                )
            ]
            restaurants_names = tree.xpath(self.selectors.get("restaurant_name_xpath"))

            # Organize data into a dictionary
            hotel_data = {
                "Hotel Name": hotel_name,
                "Address": hotel_address,
                "Description": hotel_description,
                "Rating": hotel_rating,
                "Total Reviews": total_reviews,
                "Popular Facilities": popular_facilities,
                "Restaurant Names": restaurants_names,
                # "Hotel Surroundings" : ", ".join(hotel_surroundings_data),
            }

            # Merge sub-categories data with hotel data
            hotel_data.update(sub_categories_data)

            # Check if data already exists
            # if not self.check_existing_data(hotel_data):
            self.write_to_csv(hotel_data)
            # else:
            #     print("Data already exists.")

        except etree.ParserError as e:
            print(f"Error parsing HTML: {e}")

    def write_to_csv(self, data):
        """Function to save the data into csv"""

        csv_file = "hotel_testing_data.csv"
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)
        # print(f"Data Saved to file {csv_file}.")

    def check_existing_data(self, data):
        """Function to check if data already exists in the CSV file"""

        csv_file = "hotel_testing_data.csv"
        try:
            with open(csv_file, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    existing_data_str = ",".join(row.values())
                    existing_data_hash = hashlib.md5(
                        existing_data_str.encode()
                    ).hexdigest()

                    new_data_str = ",".join(data.values())
                    new_data_hash = hashlib.md5(new_data_str.encode()).hexdigest()

                    if existing_data_hash == new_data_hash:
                        return True
        except FileNotFoundError as e:
            print(f"File not found: {e}")

        return False


if __name__ == "__main__":
    urls = [
        "https://www.booking.com/hotel/us/park-lane-new-york.en-gb.html?aid=355028&sid=da4bda249511a0264bb9e60631708902&dest_id=20088325&dest_type=city&group_adults=2&group_children=0&hapos=7&hpos=7&keep_landing=1&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&srepoch=1653886966&srpvid=ad73237a01a2015b&type=total&ucfs=1&#hp_facilities_box",
        "https://www.booking.com/hotel/sa/hyatt-regency-riyadh-olaya.en-gb.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaLUBiAEBmAEJuAEXyAEM2AEB6AEB-AEMiAIBqAIDuALn6tauBsACAdICJGYxZThhNmU5LTYxMmItNGM3Ni1hZGM2LWRlN2ZjNDA2ZWY5YdgCBuACAQ&sid=da4bda249511a0264bb9e60631708902&all_sr_blocks=211850401_327149921_3_41_0;checkin=2024-02-22;checkout=2024-02-25;dest_id=900040280;dest_type=city;dist=0;group_adults=3;group_children=0;hapos=3;highlighted_blocks=211850401_327149921_3_41_0;hpos=3;matching_block_id=211850401_327149921_3_41_0;no_rooms=1;req_adults=3;req_children=0;room1=A%2CA%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=211850401_327149921_3_41_0__248625;srepoch=1708507014;srpvid=b9623c36918f027c;type=total;ucfs=1&#tab-main",
    ]
    scraper = HotelScraper(urls)
    scraper.scrape()
