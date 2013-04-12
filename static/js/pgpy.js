$(function(){
    //initially hide the textbox
    $("#custom_folder").hide();
    $('#folder').change(function() {
      if($(this).find('option:selected').val() == "other"){
        $("#custom_folder").show();
      }else{
        $("#custom_folder").hide();
      }
    });
    $("#custom_folder").keyup(function(ev){
          var othersOption = $('#folder').find('option:selected');
          if(othersOption.val() == "other"){
            ev.preventDefault();
            //change the selected drop down text
            $(othersOption).html($("#custom_folder").val()); 
          } 
    });
    $('#form-upload').submit(function() {
        var othersOption = $('#folder').find('option:selected');
        if(othersOption.val() == "other")
        {
            // replace select value with text field value
            othersOption.val($("#custom_folder").val());
        }
    });
});
