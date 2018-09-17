var CustomInputTag = function (settings) {
    DefaultSettings = {
        select: ''
        , label_class: 'label label-info'
        , placeholder: '回车确认标签'
        , tagNumber: 5
    };
    $.extend(DefaultSettings, settings);
    init_div(DefaultSettings.select);
    init_check_value(DefaultSettings.select);
    InputTags(DefaultSettings.select);

    function find_array_index(value, word) {
        //value：input分割后的value值 word:需要删除的字符串
        for (i = 0; i < value.length; i++) {
            if (value[i] == word) {
                return i
            }
        }
        return -1
    }

    function init_div(select) {
        //初始化tag
        html = "<div class='tags-input'>";
        html += "<input type='text' placeholder='" + DefaultSettings.placeholder + "'></div>";
        $(select).before(html);
        $(select).hide()
    }

    function init_check_value(select) {
        //检查value是否有值
        tags = $(select).val();
        if (tags) {
            value_list = tags.split(',');
            var tag_html = '';
            for (i = 0; i < value_list.length; i++) {
                tag_html += create_tag(value_list[i], DefaultSettings.label_class)
            }
            $(select).prev().children('input').before(tag_html)
        }
    }

    function create_tag(value) {
        span_html = "<span class='" + DefaultSettings.label_class + "'>";
        span_html += value + "<span class='Close' data-value='";
        span_html += value + "'>&times;</span></span>";
        return span_html
    }

    function is_in(value, list) {
        for (i = 0; i < list.length; i++) {
            if (value === list[i]) {
                return true
            }
        }
        return false
    }

    function delete_tag($tags, old_value) {
        s="option[value='"+old_value+"']";
        $tags.find(s).remove()
    }

    function InputTags(select) {
        $tags = $(select);
        $(document).on('keydown', '.tags-input input', function (event) {
            if (event.keyCode == 13) {
                //Enter
                value = $.trim($(this).val());
                if (value) {
                    value_array = $tags.val();
                    if(value_array==null){
                        html = "<option value='" + value + "' selected='selected'>" + value + "</option>";
                        $tags.append(html);
                        tag_html=create_tag(value);
                        $tags.prev().children('input').before(tag_html);
                        $tags.prev().children('input').val('');
                    }
                    else if (!is_in(value, value_array)) {
                        if (value_array.length + 1 > DefaultSettings.tagNumber) {
                            message = '标签最多' + DefaultSettings.tagNumber + '个，当前' + value_array.length + '个';
                            window.alert(message);
                            $(this).val('');
                            return false
                        }
                        html = "<option value='" + value + "' selected='selected'>" + value + "</option>";
                        $tags.append(html);
                        tag_html=create_tag(value);
                        $tags.prev().children('input').before(tag_html);
                        $tags.prev().children('input').val('');
                    }
                    else{
                        message=value+'已经存在!';
                        window.alert(message);
                        return false
                    }
                }
                return false
            }
            else if (event.keyCode == 8) {
                //Backspace
                if (!$(this).val()) {
                    old_value = $(this).prev().children('.Close').attr('data-value');
                    if (old_value) {
                        delete_tag($tags, old_value);
                        $(this).prev().remove();
                    }
                }
            }
        });
        $(document).on('click', '.tags-input', function () {
            $(this).children('input').focus()
        });
        $(document).on('click', '.Close', function () {
            old_value = $(this).attr('data-value');
            delete_tag($tags, old_value);
            $(this).parent().remove()
        })
    }
};