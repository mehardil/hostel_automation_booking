from dataclasses import dataclass

@dataclass
class review_selectors():
    total_review_xpath: str ="//div[contains(@class,'reviews_panel')]//div[contains(text() ,'reviews')]/text()" 
    review_block_xpath : str = "//li[contains(@class, 'review_list')]"
    reviewer_name_xpath : str = ".//span[contains(@class, '__title')]/text()"
    reviewer_country_xpath : str = ".//span[contains(@class, '__flag')]/parent::span/text()"
    room_type_xpath : str = ".//a[contains(@class,'room-link')]//div/text()"
    stay_duration_xpath : str = ".//ul[contains(@class,'stay-date')]/li/div/text()"
    stay_date_xpath : str = ".//ul[contains(@class,'stay-date')]/li/div//span/text()"
    traveller_type_xpath : str = ".//ul[contains(@class,'traveller_type')]/li/div/text()"
    review_title_xpath : str = ".//h3[contains(@class, 'review__title')]/text()"
    review_date_xpath : str = ".//div[contains(@class,'block__right')]/div/span[contains(@class, 'date')]/text()"
    review_rating_xpath : str = ".//div[contains(@class,'bui-review-score__badge')]/text()"
    positive_review_xpath : str = ".//div[contains(@class, 'review__row')]//span[contains(@class, 'review__prefix') and contains(@class, 'green')]/following-sibling::span[contains(@class,'review__body')]/text()"
    negative_review_xpath : str = ".//div[contains(@class, 'review__row')]//span[contains(@class, 'review__prefix') and not(contains(@class, 'green'))]/following-sibling::span[contains(@class,'review__body')]/text()"
    hotel_response_xpath : str = ".//div[contains(@class, 'review')]//span[contains(@class, 'response__body')]/following-sibling::span/text()"
    review_photos_xpath : str = ".//ul[contains(@class,'review-block__photos')]/li"


@dataclass
class hotel_data_selectors():
    hotel_name_xpath : str = "//div[contains(@id, 'hotel_name')]//h2/text()"
    hotel_address_xpath : str = "//p[contains(@class,'address')]/span[contains(@data-node_tt_id, 'location')]/text()"
    hotel_description_xpath : str = "//div[contains(@class,'description')]//div[contains(@data-capla-component-boundary, 'DescriptionDesktop')]//p/text()"
    total_reviews_xpath : str = "//a[contains(@data-testid, 'reviews')]//div/span/text()"
    hotel_rating_xpath : str = "//div[contains(@data-testid,'review-score-component')]/div/text()"
    hotel_stars_rating_xpath : str = "//span[contains(@data-testid, 'rating-stars')]/span"
    sub_categories_xpath : str = "//div[contains(@data-testid, 'PropertyReviewsRegionBlock')]//div[contains(@data-testid, 'review-subscore')]//div[@id]//span/text()"
    sub_categories_rating_xpath : str = "//div[contains(@data-testid, 'PropertyReviewsRegionBlock')]//div[contains(@data-testid, 'review-subscore')]//div[@id]//span[not(text()='')]/parent::div/parent::div/following-sibling::div/div/text()"

    popular_facilities_xpath : str = "//div[contains(@class, 'popular_facilities ')]//li//span[text()]/text()"

    hotel_surroundings_xpath : str = "//section[contains(@id, 'surroundings_block')]//li//span/div/div[text()]/text()"
    hotel_surroundings_distance_xpath : str = "//section[contains(@id, 'surroundings_block')]//li//span/div/div[@class='']/div/text()"
    
    # Restaurants XPaths
    restaurants_xpath : str = "//div[@data-testid='restaurant-card']"
    restaurant_name_xpath : str = "//div[@data-testid='restaurant-card']/div/div/text()"
    restaurant_cuisines_xpath : str = "//div[@data-testid='restaurant-card']//div[text() = 'Cuisine']/following-sibling::div/text()"
    
    questions_xpath : str = "//div[contains(@class, 'faq__content')]//li//h3"
    