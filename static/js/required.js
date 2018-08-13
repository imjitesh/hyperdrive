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
        var _id = (window.location.href.split('/').slice(-1)[0]) ? (window.location.href.split('/').slice(-1)[0]) : 1
        var f = new File([document.documentElement.outerHTML], _id);
        var formData = new FormData();
        formData.append('html_file', f);
        $.ajax({
            url: 'save',
            type: "POST",
            processData: false,
            contentType: false,
            data: formData,
            success: function(result) {
                if(JSON.parse(result)['is_created']){
                    window.location = JSON.parse(result)['_id'];
                }
                else{
                    console.log("is_updated");
                }
            },
            error: function() {
                console.log("something happened");
            }
        });
    })

    $('body').on('click','#publish', function(){
        var head = "<!DOCTYPE html><html lang='en'><head>"+$('head').html()+"</head>"
        var body = "<body><div class='container-fluid data-container' style='margin:0 auto;width:75%;'>"+$('.data-container').html().replace(/<textarea/g,"<textarea disabled")+"</body></html>"
        var fileName = document.title.replace(/[\W_]+/g,"_") +".html"
        var htmlContent = [head+body];
        console.log(htmlContent);
        var bl = new Blob(htmlContent, {type: "text/html"});
        var encodedUri = URL.createObjectURL(bl);
        var link = document.getElementById('publish');
        link.setAttribute("href",encodedUri);
        link.setAttribute("download",fileName);
        })

});