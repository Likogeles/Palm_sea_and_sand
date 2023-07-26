class Place:
    id = None
    osmid = None
    type_ = None
    object_ = None
    name = None
    lat = None
    lon = None
    geometry = None
    city = None
    historic = None
    addr_street = None
    addr_housenumber = None
    start_date = None
    opening_hours = None
    phone = None
    contact_website = None
    building_levels = None
    wikipedia = None
    contact_phone = None
    ref_temples_ru = None
    contact_email = None
    website = None
    description = None
    contact_vk = None
    service_times = None
    contact_facebook = None
    contact_instagram = None
    contact_twitter = None
    contact_youtube = None
    email = None
    class_ = None
    is_culture = None
    is_historic = None
    is_religious = None
    is_art = None
    is_natural = None
    popularity = None
    time = None

    def __str__(self):
        return f"{self.id}: {self.osmid} {self.type_} {self.object_} {self.name} {self.lat} {self.lon} {self.geometry} {self.city} {self.historic} {self.addr_street}"\
                f"{self.addr_housenumber} {self.start_date} {self.opening_hours} {self.phone} {self.contact_website} {self.building_levels} {self.wikipedia}"\
                f"{self.contact_phone} {self.ref_temples_ru} {self.contact_email} {self.website} {self.description} {self.contact_vk} {self.service_times}"\
                f"{self.contact_facebook} {self.contact_instagram} {self.contact_twitter} {self.contact_youtube} {self.email} {self.class_}"\
                f"{self.is_culture} {self.is_historic} {self.is_religious} {self.is_art} {self.is_natural} {self.popularity} {self.time}"

    def __init__(self, id, osmid, type_, object_, name, lat, lon, geometry, city, historic, addr_street,
                 addr_housenumber, start_date, opening_hours, phone, contact_website, building_levels, wikipedia,
                 contact_phone, ref_temples_ru, contact_email, website, description, contact_vk, service_times,
                 contact_facebook, contact_instagram, contact_twitter, contact_youtube, email, class_,
                 is_culture, is_historic, is_religious, is_art, is_natural, popularity, time):
        self.time = time
        self.popularity = popularity
        self.is_natural = is_natural
        self.is_art = is_art
        self.is_religious = is_religious
        self.is_historic = is_historic
        self.is_culture = is_culture
        self.class_ = class_
        self.email = email
        self.contact_youtube = contact_youtube
        self.contact_twitter = contact_twitter
        self.contact_instagram = contact_instagram
        self.contact_facebook = contact_facebook
        self.contact_phone = contact_phone
        self.ref_temples_ru = ref_temples_ru
        self.contact_email = contact_email
        self.website = website
        self.description = description
        self.contact_vk = contact_vk
        self.service_times = service_times
        self.wikipedia = wikipedia
        self.building_levels = building_levels
        self.contact_website = contact_website
        self.phone = phone
        self.opening_hours = opening_hours
        self.start_date = start_date
        self.addr_housenumber = addr_housenumber
        self.addr_street = addr_street
        self.historic = historic
        self.city = city
        self.geometry = geometry
        self.lon = lon
        self.lat = lat
        self.name = name
        self.object_ = object_
        self.type_ = type_
        self.osmid = osmid
        self.id = id
