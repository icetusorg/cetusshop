
/*========== Left Nav ===========*/
 

function product_search_filter()
{
jQuery('.top_search_input').bind('keydown', function(e)
        {
                if (e.keyCode == 13)
                {
                        name = jQuery(this).attr('name');
                        var search = jQuery(this).attr('value');
                        url = jQuery('base').attr('href') + 'index.php?route=product/search';

                        if (search)
                        {
                                url += '&search=' + encodeURIComponent(search);
                        }                       
                        location = url;
                }
        });
}


function remove_info_box()
{
        jQuery('.success img, .warning img, .attention img, .information img').live('click', function() {
                jQuery(this).parent().fadeOut('slow', function() {
                        jQuery(this).remove();
                });
        });
}


//function to style checkbox and radio buttons
function inputs_skin(){
  jQuery('.select_skin select').live('change', function(){
    var the_select = jQuery(this);
    the_span = jQuery(this).parent().find('.selected_value');
    the_span.text(the_select.find('option:selected').text());        
    });
}
        

//function  increase/ decrease product qunatity buttons +/-
function change_qty(container){ 
        var container = container;      
        var input = jQuery(container).find('input:text');
        default_val = jQuery(input).val();
        j = default_val;
        remove = jQuery(container).find('span.minus_qty');
        add = jQuery(container).find('span.plus_qty');

        add.on('click', function(){
                j++;
                jQuery(input).val(j);
        });

        remove.on('click', function(){
                if(j > 1)
                {
                        j--;
                jQuery(input).val(j);
                } else{
                        j = 1;
                }
        });
        
        input.blur(function(){          
                if(jQuery(this).val() <= 0){
                        j = 1;
                        jQuery(this).val(1);
                }else{
                        j = jQuery(this).val();
                }
        });
}



jQuery(document).ready(function(){      
        inputs_skin();
        product_search_filter();
        remove_info_box();      

 

        //increase/ decrease product qunatity buttons +/- in cart.html table
        if(jQuery('.subDropdown')[0]){
                jQuery('.subDropdown').click(function(){
                        jQuery(this).toggleClass('plus');
                        jQuery(this).toggleClass('minus');
                        jQuery(this).parent().find('ul').slideToggle();
                });
        }
        

        


});

/*=============End Left Nav=============*/