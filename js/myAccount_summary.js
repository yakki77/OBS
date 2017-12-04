var modalConfirm = function(callback){

  $("#transfer").on("click", function(){

  	$("#fromjs").text($("#from option:selected").text());
    $("#tojs").text($("#to").val());
    $("#amountjs").text($("#amount").val());
    $("#currencyjs").text($("#currency option:selected").text());

    $("#mi-modal").modal('show');
    $("#parent").show()
    $("#message").hide()
    $("#modal-button").show()

  });

  $("#modal-btn-si").on("click", function(){
    callback(true);
    $("#mi-modal").modal('show');
  });

  $("#modal-btn-no").on("click", function(){
    callback(false);
    $("#mi-modal").modal('hide');
  });
};

modalConfirm(function(confirm){
  if(confirm){
    //Acciones si el usuario confirma
    $("#parent").hide()
    $("#message").show()
    $("#modal-button").hide()
  }
});

var addAccount = function(callback){
  $("#addAccount").on("click", function(){
    $("#add-popup").modal("show")
    $("#accountInfo").show()
    $("#added").hide()
    $("#addButton").show()
  })

  $("#addYes").on("click", function(){
    callback(true)
    $("#add-popup").modal("show")
  })

  $("#addNo").on("click", function(){
    callback(false)
    $("#add-popup").modal("hide")
  })
}

addAccount(function(confirm){
  if (confirm){
    $("#accountInfo").hide()
    $("#added").show()
    $("#addButton").hide()
  }
})
