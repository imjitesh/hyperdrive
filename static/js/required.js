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
        if(this.className == 'title-area'){
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
        console.log($('input#image_url').val());
        $(image_holder).attr('src', $('input#image_url').val());
        console.log(image_holder);
    })

    $('.save').on('click', function() {
        $.ajax({
            url: "save",
            type: "GET",
            data: {
                _id: window.location.href.split('/').slice(-1)[0],
                row_data:$(".data-container").html()
            },
            success: function(response) {
            },
            error: function(xhr) {
            }
        });
    })

});