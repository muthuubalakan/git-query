function iterator(div, resp) {
    $.each(resp,function(index,value){ 
    $.each(value, function(index2, value2) {

                div.append("<p>" + value2 + "</P>")
    }); 

});
}


function getRepo(){
    let username = $('#user').val();

    $.post(
        '/api/v1/gitsearch',
        {user: username},
        function(response, status){
            response.forEach(element => {
                $('#respdisplay').html('<button type="button" class="btn btn-primary btn-block">' + element.name +"</button> ");

            });

            console.log(response, status)
        }
    )
}