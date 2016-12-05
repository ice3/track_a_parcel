function delete_parcel(parcel_number){
  console.log("delete parcel : ", parcel_number)
  $.ajax({
    url: '/api/parcel/'+parcel_number ,
    type: 'DELETE',
    success: function(result) {
      console.log(result);
      var target = $('#panel-'+parcel_number);
      target.hide('slow', function(){target.remove();});
    }
  });
}

function toggle_received(parcel_number){
  console.log("update parcel receive status : ", parcel_number)
  $.ajax({
    url: '/api/parcel/'+parcel_number ,
    type: 'UPDATE',
    data: {'toggle_received': true},
    success: function(result) {
      if(result.received){
        $('#received-'+parcel_number).addClass("text-success");
      }
      else{
        $('#received-'+parcel_number).removeClass("text-success");
      }
    }
  });
}


function add_parcel(event){
    event.preventDefault();

    $.ajax({
        url: '/api/parcel/',
        type: 'POST',
        dataType: 'json',
        data: $('#formAddParcel').serialize(),
        success: function(data) {
          console.log("parcel successfully added", data);
          if(data.added){
            $('#parcels').append(data.html);
          } else {
            $('#panel-'+data.number).replaceWith(data.html)  ;
          }
          $("#divFormAddParcel").collapse("hide");
        }
    });
};