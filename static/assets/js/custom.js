
$(document).ready(function() {

        $(window).load(function() {
        	file_object = $("#select_file");
        	$.getJSON($("#select_file").attr('action'),function(json){
  	      		$.each(json.message,function(n,value){
  	      			file_object.append("<option value='"+value+"'>"+value+"</option>"); 
  	            });
  	      	});
        });
        
       
        $("#select_file").change(function(){
        	
        })
});
