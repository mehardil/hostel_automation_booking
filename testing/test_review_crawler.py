import pytest

urls = [
    "https://www.booking.com/hotel/us/park-lane-new-york.en-gb.html?aid=355028&sid=da4bda249511a0264bb9e60631708902&dest_id=20088325&dest_type=city&group_adults=2&group_children=0&hapos=7&hpos=7&keep_landing=1&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&srepoch=1653886966&srpvid=ad73237a01a2015b&type=total&ucfs=1&#tab-reviews"
]
def hostel_cc_name(urls):
    results = []
    for url in urls:
        cc = url.split("/")[4]
        hotel_name = url.split("/")[5].split(".")[0]
        results.append((cc, hotel_name))
    return results

class TestHostelCCName:
    #cc testing
    def test_answer_cc(self):
        if hostel_cc_name(urls)[0][0] != "us":
            raise SystemExit(1)
    #hostelname testing
    def test_answer_hostelname(self):
        assert hostel_cc_name(urls)[0][1] == "park-lane-new-york"

