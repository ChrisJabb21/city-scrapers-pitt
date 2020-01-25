from city_scrapers_core.constants import NOT_CLASSIFIED
from city_scrapers_core.items import Meeting
from city_scrapers_core.spiders import CityScrapersSpider

class PaEnergySpider(CityScrapersSpider):
    name = "pa_energy"
    agency = "PA Department of Environmental Protection"
    timezone = "America/New_York"
    allowed_domains = ["www.ahs.dep.pa.gov"]
    start_urls = ["http://www.ahs.dep.pa.gov/CalendarOfEvents/Default.aspx?list=true"]
    custom_settings = {'ROBOTSTXT_OBEY': False}


    

    def parse(self, response):
        """
        `parse` should always `yield` Meeting items.

        Change the `_parse_title`, `_parse_start`, etc methods to fit your scraping
        needs.
        """
        for item in response.css(".meetings"):
            meeting = Meeting(
                title=self._parse_title(item),
                description=self._parse_description(item),
                classification=self._parse_classification(item),
                start=self._parse_start(item),
                end=self._parse_end(item),
                all_day=self._parse_all_day(item),
                time_notes=self._parse_time_notes(item),
                location=self._parse_location(item),
                links=self._parse_links(item),
                source=self._parse_source(response),
            )

            meeting["status"] = self._get_status(meeting)
            meeting["id"] = self._get_id(meeting)

            yield meeting

    def _parse_title(self, item):
        """Parse or generate meeting title."""

        title =  item.css("#ContentPlaceHolder2_ctl00_titleCell::text").extract_first().strip(u'\xa0')
        
        return title
    

    def _parse_description(self, item):
        """Parse or generate meeting description."""

        description = item.css("#ContentPlaceHolder2_ctl00_descriptionDataCell::text").extract()

        
        return description

    def _parse_classification(self, item):
        """Parse or generate classification from allowed options."""
        return NOT_CLASSIFIED

    def _parse_start(self, item):
        """Parse start datetime as a naive datetime object."""
        return None

    def _parse_end(self, item):
        """Parse end datetime as a naive datetime object. Added by pipeline if None"""
        return None

    def _parse_time_notes(self, item):
        """Parse any additional notes on the timing of the meeting"""
        return ""

    def _parse_all_day(self, item):
        """Parse or generate all-day status. Defaults to False."""
        return False

    def _parse_location(self, item):
        """Parse or generate location."""

        location =  item.css("#ContentPlaceHolder2_ctl00_locationDataCell::text").extract_first().replace('\xa0',' ')
        
        return location
        #{
            #"address": "",
            #"name": "",
        #}

    def _parse_links(self, item):
        """Parse or generate links."""
        return [{"href": "", "title": ""}]

    def _parse_source(self, response):
        """Parse or generate source."""
        return response.url
