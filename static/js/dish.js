//choose restaurant
$(window).ready(function() {
    if (window.location.href.indexOf('process_order') >= 0){
        $("ul.not_book_people>li").attr('onclick','as($(this).text())');

        $(".booked_order>.order_r.>.order_list>li>span.food_price").after("<span class='order_cancel' style='color:blue;'>取消</span>");

        $('.order_cancel').click( function() {
            cancel_order($(this).parent().attr('id'))
        });
        //$('.totol_price').html("共计:" + flush_price() + "元")
        $('.total_price').each( function (index){
            flush_price(this) 
        });
        $('.finished_order').masonry({
            itemSelector: '.order_r',
        });
    };

    if (window.location.pathname == '/'){
        $('.menu_list>li>span').click( function() {
            //choose_food($(this).attr('id'))
        });

        $('.restaurant_list>li').click( function() {
            choose_restaurant($(this).attr('id'))
        });
        
        $(".order_booked>ul>li").append("<span class='order_cancel' style='color:blue;'>取消</span>");
        $('.order_cancel').click( function() {
            cancel_order($(this).parent().attr('id'))
        });
    };
});

function choose_restaurant(restaurant_id){
    $('.restaurant_list>li').removeClass('active');
    $('.restaurant_list>li#'+restaurant_id).addClass('active');
    $.ajax({
        type:"GET",
        url:"/j/food_list?restaurant="+restaurant_id,
        cache:"false",
        dataType:"json",
        success:function(result){
            if (result !='False'){
                $('#new_food').remove()
                menu_list = $('.menu_list')
                $('.menu_list>li').remove()
                $.each(result, function(index, value){
                    food = value.fields;
                    li = "<li id='f_" + value.pk + "' onclick='choose_food(" + value.pk + ")'>" + 
                    "<span class='dish_name'>"+ food.name + 
                    "</span><span class='price'>" + food.price + 
                    "元</span></li>";
                    menu_list.append(li)
                });
                menu_list.after("<div id='new_food'><p>没有您需要的食物吗？您可以自行添加。</p><p><label for='new_food_name'>食物名:</label><input type='text' id='new_food_name'><label for='new_food_price'>价格:</label><input type='text' id='new_food_price' max_length='5' </label>元<input type='button' onclick='new_food()' value='提交'></p>")
            }else{
                alert("food_list 获取数据失败");
            }
           }
    })
} 
//choose food
function choose_food(_food_id) {
    $('.menu_list>li.active').removeClass('active');
    $('#f_'+_food_id).addClass('active');
    $('.food_order').remove();
    restaurant_id = $('.restaurant_list>li.active').attr('id');
    restaurant_name = $('.restaurant_list>li.active').text();
    food_id = "f_" + _food_id;
    food_name = $('#'+food_id +'>span.dish_name').text();
    price = $('#'+food_id +'>span.price').text();

    food_order = "<div class='food_order'>" +  
    "<span class='order_restaurant' id='" + restaurant_id + "'>" +
    restaurant_name + "</span>" + "<span class='order_food' id='" + 
    food_id + "'>" + food_name + "</span>" + "<span class='order_price'>" +
    price + "</span></div>"
    $('.order_confirm').prepend(food_order);
};
//submit order
function submit_order() {
    food_id = $('.order_food').attr('id');
    date = $('.Wdate').val();
    dish_character = $('select.dish_character').val();
    remark = $('#order_remark').val();
    if (remark.length >50){
        alert("备注字数不能超过50个字,您的字数:" + remark.length)
        return false
    }
    //console.log(food_id + " date:" +date + " fc:"+dish_character);
    //f_7 2011-12-22 1
    //console.log(remark);
    if (food_id==undefined){alert("请选择食物");return;}
    if (date==''){alert("请选择日期");return;}
    if (dish_character=='u'){alert("请选择餐类型(中餐或晚餐)");return;}
    $.ajax({
        type:"POST",
        url:"/j/order_book_confirm",
        data:{"food_id":food_id, "date":date, "dish_character":dish_character, "remark":remark},
        cache:"false",
        dataType:"json",
        success:function(data){
            if (data!="Fail"){
                $('.food_order').html('点餐成功');
                $('.menu_list>li.active').removeClass('active');
                $('.Wdate').val('');
                $('#order_remark').val('');
                remark = data.remark ? "<b>备注:" + data.remark + 
                         "</b></br>":''
                console.log(remark)
                order_new = "<li class='order_new' id='order_"+ 
                data.order_id + "_" + 
                data.order_date + "_" + data.character + "'>" + 
                data.restaurant + " " + data.food_name + " " + 
                data.food_price + "元</br>" + remark + 
                data.order_date + " " +  
                data.dish_character + "</li></br>";
                $('.order_booked>ul').prepend(order_new);
                }
            else{
                $('.food_order').html('点餐失败');
            }
        }
    });

};

function cancel_order(order_id) {
    console.log(order_id);
    _order_id = order_id.split('_',2)[1];
    $.ajax({
    type:"POST",
    url:"/j/order_cancel",
    data:{"order_id":_order_id},
    cache:"false",
    success:function(data){
        if (data=="Success"){
            $('#'+order_id).attr('style','color:red');
            $('#'+order_id +'>span.order_cancel').remove()
            if (window.location.href.indexOf('process_order') >= 0){
                item = $('#' + order_id)
                item.attr('id','order_' + _order_id + '_a')
                flush_price(item.parent().siblings('.total_price'))
            }
        }
        else{
            alert("取消失败");
        }
    }
    });
}

function as(value){
    $("#not_book_name").attr('value',value);
}

function avatar(){
    value = $("#not_book_name").attr('value');
    
    if (!value){
        alert("请输入用户名字")
        return false;
    }
    window.open('/avatar?not_book_name=' + value);
    return false;
}

function flush_price(_t) {
    var order_list = $(_t).prev().prev().children()
    o_status = $(_t).parent().parent().attr('class')[0]
    var total_price = 0 
    $.each(order_list, function(index, value) {
        order_status = $(value).attr('id').split('_',3)[2]
        if (order_status == o_status ){
            total_price += parseFloat($(value).children('.food_price').text())
        }
    })
    //$(this).siblings('.total_price').remove()
    $(_t).html("共计:" + total_price + "元")
}

function confirm_order(_t){
    var c_order = new Array()
    $(_t).prev().children().each( function(index, value) {
        temp_id = $(value).attr('id').split('_')
        if (temp_id[2] == 'b'){
        c_order.push(temp_id[1])
        }
    })
    if (c_order.length != 0){
        c_order_string = c_order.join(',')
        $.ajax({
            type:"POST",
            url:"/j/confirm_order",
            data:{"confirm_orders":c_order_string},
            cache:"false",
            success:function(result){
                if (result=='Success'){
                    $(_t).prev().children().each( function(index, value) {
                        temp_id = $(value).attr('id').split('_')
                        if (temp_id[2] == 'a'){
                            $(value).remove()
                        }else if(temp_id[2] == 'b'){
                            $(value).attr('id', 'order_' + temp_id[1] + '_c')
                        }
                        console.log(
                        $(value).children('span.order_cancel')
                        )
                        $(value).children('span.order_cancel').remove()
                    })
                    $(_t).after("<input type='submit' value='完成' class='finish_order' onclick='finish_order(this)'>")
                    r = $(_t).parent()
                    r.attr("style","background:#d7f294;")
                    $(".confirmed_order").prepend(r)
                    $(_t).remove()
                }else{
                    alert("error")
                }
            }
        })
    }else{
        alert("好像没有合法的菜单, 刷新下网页吧。")
    }
}

function finish_order(_t){
    var f_order = new Array()
    $(_t).prev().children().each( function(index, value) {
        temp_list = $(value).attr('id').split('_')
        if (temp_list[2] == 'c'){
        f_order.push(temp_list[1])
        }
    })
    if (f_order.length != 0){
        f_order_string = f_order.join(',')
        $.ajax({
            type:"POST",
            url:"/j/finish_order",
            data:{"finish_orders":f_order_string},
            cache:"false",
            success:function(result){
                if (result=='Success'){
                    r = $(_t).parent()
                    r.attr("style","background:#ddd;")
                    $(".finished_order").prepend(r).masonry('reload')
                    $(_t).remove()
                }else{
                    alert("error")
                }
            }
        })
    }else{
        alert("好像没有合法的菜单, 刷新下网页吧。")
    }
}

function reg_check(){
    login_p = $('#login_password').val()
    confirm_p = $('#confirm_password').val()
    real_n = $('#real_name').val()
    login_n = $('#login_name').val()
    if (login_n==''){
        alert('未填用户名')
        return false
    }
    if (real_n==''){
        alert('未填真实姓名')
        return false
    }
    if (login_p==''){
        alert('密码不能为空')
        return false;
    }
    if (login_p == confirm_p){
        $(".reg_form").submit()
    }else{
        alert('密码不一致');
        return false;
    }
}

function new_food(){
    var food_pk = '' 
    restaurant = $('ul.restaurant_list>li.active').attr('id').split('_')[1]
    food_name = $('#new_food_name').val()
    _food_price = $('#new_food_price').val()
    if (restaurant != '' && food_name != '' && _food_price !='' ){
        food_price = parseFloat(_food_price)
        $.ajax({
            type:"POST",
            url:"/j/new_food",
            data:{"restaurant":restaurant, 'food_name':food_name, 'food_price':food_price},
            cache:"false",
            success:function(result){
                if (result=='Fail'){
                    alert("error")
                }else{
                    food = result.split(',');
                    new_food_info = "<li id='f_" + food[0] + "' style='border:1px solid #d7f294;' onclick='choose_food(" 
                    + food[0] + ")'><span class='dish_name'>" + food[1] + "</span><span class='price'>" + 
                    food[2]  + "元</span></li>";
                    $('.menu_list').append(new_food_info);
                }
            }
        })
        $('#new_food_name').val('');
        $('#new_food_price').val('');
    }else{
        alert("请输入食物名称和价格")
    }
}
