let image_holder = {};
$(document).ready(function() {
    $.fn.clickToggle = function(func1, func2) {
        var funcs = [func1, func2];
        this.data('toggleclicked', 0);
        this.click(function() {
            var data = $(this).data();
            var tc = data.toggleclicked;
            $.proxy(funcs[tc], this)();
            data.toggleclicked = (tc + 1) % 2;
        });
        return this;
    };

    $('.add_data_button').clickToggle(
        function() {
            $('.add_icons').show();
            $(this).css({
                'transform': 'rotate(45deg)'
            });
        },
        function() {
            $('.add_icons').hide();
            $(this).css({
                'transform': 'rotate(0deg)'
            });
        })

    $('img.type1').on('click', function() {
        $('.data-container').append($('.type1-container').html());
    })
    $('img.type2').on('click', function() {
        $('.data-container').append($('.type2-container').html());
    })
    $('img.type3').on('click', function() {
        $('.data-container').append($('.type3-container').html());
    })
    $('img.type4').on('click', function() {
        $('.data-container').append($('.type4-container').html());
    })
    $('img.type5').on('click', function() {
        $('.data-container').append($('.type5-container').html());
        $('.ba-slider').each(function() {
            var cur = $(this);
            var width = cur.width() + 'px';
            cur.find('.resize img').css('width', width);
            drags(cur.find('.handle'), cur.find('.resize'), cur);
        });
    })

    $(document).on('keyup', 'textarea', function autosize(e) {
        var el = this;
        el.innerHTML = $(this).val();
        if (this.className == 'heading-area' && e.keyCode == 8 && $(this).val() == "") {
            console.log("delete data row now");
            if (confirm("Delete this segment?")) {
                $(this).parent().parent().remove();
            }
        }
        if (this.className == 'title-area') {
            document.title = $(this).val();
        }

        setTimeout(function() {
            el.style.cssText = 'height:' + el.scrollHeight + 'px';
        }, 0);
    })

    $(document).on('click', 'img.img-show', function() {
        image_holder = this;
    })

    $(document).on('click', '.update-image', function() {
        $(image_holder).attr('src', $('input#image_url').val());
        $('input#image_url').val("");
    })

    $('.save').on('click', function() {
        console.log($(".data-container .data-row")[0]);
        var _id = (window.location.href.split('/').slice(-1)[0]) ? (window.location.href.split('/').slice(-1)[0]) : 1
        $.ajax({
            url: "save",
            type: "GET",
            data: {
                _id: _id,
                row_data: $(".data-container").html(),
                title: document.title
            },
            success: function(response) {
                if (window.location.href.split('/').slice(-1)[0] == "") {
                    window.location = "/" + response;
                } else {
                    return false;
                }
            },
            error: function(xhr) {}
        });
    })

});