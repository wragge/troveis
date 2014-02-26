$(function() {

	var zones = ['newspaper', 'book', 'article', 'map', 'music', 'picture', 'collection', 'list'];
	$.getJSON('/newspaper.json', function(data) {
		var img_url, title, citation, url;
		if (typeof data['pdf'] !== 'undefined') {
			img_url = data['pdf'].replace('/print', '');
		}
		title = data['heading'];
		url = data['troveUrl'];
		var date = moment(data['date'], 'YYYY-MM-DD').format('D MMM YYYY');
		var newspaper = data['title']['value'];
		citation = date + ', ' + newspaper;
		display_item('#newspaper', img_url, title, citation, url);
	});

	$.getJSON('/book.json', function(data) {
		var img_url, title, citation, url, contributors;
		img_url = get_img(data);
		title = data['title'];
		url = data['troveUrl'];
		if (typeof data['contributor'] !== 'undefined') {
			contributors = data['contributor'].join(', ');
		}
		if (typeof contributors !== 'undefined') {
			citation = contributors + '<br>' + data['issued'];
		} else {
			citation = data['issued'];
		}
		display_item('#book', img_url, title, citation, url);
	});

	$.getJSON('/article.json', function(data) {
		var img_url, title, citation, url, contributors;
		img_url = get_img(data);
		title = data['title'];
		url = data['troveUrl'];
		if (typeof data['contributor'] !== 'undefined') {
			contributors = data['contributor'].join(', ');
		}
		if (typeof contributors !== 'undefined') {
			citation = contributors + '<br>' + data['issued'];
		} else {
			citation = data['issued'];
		}
		display_item('#article', img_url, title, citation, url);
	});

	$.getJSON('/map.json', function(data) {
		var img_url, title, citation, url, contributors;
		img_url = get_img(data);
		title = data['title'];
		url = data['troveUrl'];
		if (typeof data['contributor'] !== 'undefined') {
			contributors = data['contributor'].join(', ');
		}
		if (typeof contributors !== 'undefined') {
			citation = contributors + '<br>' + data['issued'];
		} else {
			citation = data['issued'];
		}
		display_item('#map', img_url, title, citation, url);
	});

	$.getJSON('/sound.json', function(data) {
		var img_url, title, citation, url, contributors;
		img_url = get_img(data);
		title = data['title'];
		url = data['troveUrl'];
		if (typeof data['contributor'] !== 'undefined') {
			contributors = data['contributor'].join(', ');
		}
		if (typeof contributors !== 'undefined') {
			citation = contributors + '<br>' + data['issued'];
		} else {
			citation = data['issued'];
		}
		display_item('#music', img_url, title, citation, url);
	});

	$.getJSON('/picture.json', function(data) {
		var img_url, title, citation, url, contributors;
		img_url = get_img(data);
		console.log(img_url);
		title = data['title'];
		url = data['troveUrl'];
		if (typeof data['contributor'] !== 'undefined') {
			contributors = data['contributor'].join(', ');
		}
		if (typeof contributors !== 'undefined') {
			citation = contributors + '<br>' + data['issued'];
		} else {
			citation = data['issued'];
		}
		display_item('#picture', img_url, title, citation, url);
	});

	$.getJSON('/archive.json', function(data) {
		var img_url, title, citation, url, contributors;
		img_url = get_img(data);
		title = data['title'];
		url = data['troveUrl'];
		if (typeof data['contributor'] !== 'undefined') {
			contributors = data['contributor'].join(', ');
		}
		if (typeof contributors !== 'undefined') {
			citation = contributors + '<br>' + data['issued'];
		} else {
			citation = data['issued'];
		}
		display_item('#collection', img_url, title, citation, url);
	});

	$.getJSON('/list.json', function(data) {
		var img_url, title, citation, url;
		title = data['title'];
		url = data['troveUrl'];
		var creator = data['creator'].replace('public:', '');
		var date = moment(data['created'].substr(0,10), 'YYYY-MM-DD').format('D MMM YYYY');
		citation = creator + '<br>' + date;
		display_item('#list', img_url, title, citation, url);
	});

	function get_img(data) {
		var img_url;
		if (typeof data['identifier'] !== 'undefined') {
			$.each(data['identifier'], function(key, id) {
				if (id['linktype'] == 'thumbnail') {
					img_url = id['value'];
				}
			});
		}
		return img_url;
	}

	function display_item(id, img_url, title, citation, url) {
		if (typeof img_url !== 'undefined') {
			$(id).loadTemplate("/static/templates/item_picture.html",
				{
					title: title,
					citation: citation,
					img_url: img_url,
					url: url
				});
        } else {
			$(id).loadTemplate("/static/templates/item.html",
				{
					title: title,
					citation: citation,
					url: url
				});
        }
	}

});