/*
 * Bootstrap Image Gallery JS Demo 3.0.0
 * https://github.com/blueimp/Bootstrap-Image-Gallery
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint unparam: true */
/*global window, document, blueimp, $ */

$(function () {
    'use strict';

    // Load demo images:
    var linksContainer = $('#links'),
        baseUrl;
    // Add the demo images as links with thumbnails to the page:
    for (var i=1; i<10; i++) {
    	var col = $('<div class="col-lg-3 col-sm-4 col-xs-6"/>');
    	$('<a class="thumbnail" />')
        .append($('<img class="thumbnail_img">').prop('src', '/static/gallery/images/image-iso'+i+'.png'))
        .prop('href', '/static/gallery/images/image-iso'+i+'.png')
        .prop('title', 'image-iso'+i+'.png')
        .attr('data-gallery', '')
        .appendTo(col);
    	col.appendTo(linksContainer);
    }
    
    

    $('#borderless-checkbox').on('change', function () {
        var borderless = $(this).is(':checked');
        $('#blueimp-gallery').data('useBootstrapModal', !borderless);
        $('#blueimp-gallery').toggleClass('blueimp-gallery-controls', borderless);
    });

    $('#image-gallery-button').on('click', function (event) {
        event.preventDefault();
        blueimp.Gallery($('#links div a'), $('#blueimp-gallery').data());
    });

});
