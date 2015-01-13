return if not $('body').hasClass('project-search')


_get = (name) ->
	# Retrieve the value of a GET parameter
	(new RegExp("[?&]#{name}=([^&$]*)").exec(location.search) or [0, null])[1]

# Pin images
PIN_USER = "#{STATIC_URL}styl/glyphs/user-location.png"

# Cache some elements for better performance
form = $('#search-results form')[0]
search_results = $('#search-results ul')


class ProjectSearch

	constructor: (user_lat, user_lng) ->
		center = new google.maps.LatLng(user_lat, user_lng)

		# Create and render the Google Maps widget
		map_canvas = $('<div/>')[0]
		$('#map').append(map_canvas)
		map = @map = new google.maps.Map map_canvas, center: center, zoom: 13

		# Mark the user into it
		@user_marker = new google.maps.Marker
			map: map,
			position: center,
			icon: PIN_USER,

		# Mark projects' locations
		search_results.children('.project').each ->
			new google.maps.Marker
				map: map,
				position: new google.maps.LatLng(
					+@getAttribute('data-lat'), +@getAttribute('data-lng'))

		# Initialize a geocode autocomplete on the search form
		autocomplete = new google.maps.places.Autocomplete form.q,
			types: ['geocode'],

		# Fill latitude and longitude fields with geocode
		$(form).on 'submit', (e) ->
			if @lat.value and @lng.value
				return

			e.preventDefault()  # Stop the submit

			geocoder = new google.maps.Geocoder()
			geocoder.geocode address: @q.value, (results, status) =>
				if status != google.maps.GeocoderStatus.OK
					alert('Endereço não encontrado: ' + status)
					return

				location = results[0].geometry.location
				@lat.value = location.lat()
				@lng.value = location.lng()
				@submit()


# Initialize ProjectSearch with geo coords from URL
new ProjectSearch +_get('lat'), +_get('lng')
