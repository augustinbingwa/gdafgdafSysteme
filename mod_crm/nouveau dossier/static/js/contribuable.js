
//-----------------------------------------------
// CONTRIBUABLE - PERSONNE MORALE - GESTION TYPE DE CARACTERE : COMMERCIAL OU sans but LUCRATIF
//-----------------------------------------------
function OnTypeCaractereChanged(){
	
    var selectedValue = $('#id_type_caractere').val();

    switch(parseInt(selectedValue, 10)) {
      case 0: // COMMERCIAL
        $('#id_rc_numero').attr("disabled", false);
        $('#id_nif_numero').attr("disabled", false); 
        break;

      case 1: // LUCRATIF
        $('#id_nif_numero').attr("disabled", false); 

        $('#id_rc_numero').attr("disabled", true); 
        $('#id_rc_numero ').val('');
        break;
      
      case 2: // ASSOCIATION
        $('#id_nif_numero').attr("disabled", true); 
        $('#id_nif_numero ').val('');
        
        $('#id_rc_numero').attr("disabled", true); 
        $('#id_rc_numero ').val('');    
        break;
      }
}

//---------------------------------------------
//---------------- UPLOAD FILE JS -------------
//---------------------------------------------
function bs_input_file() {
  $(".input-file").before(
    function() {
      if ( ! $(this).prev().hasClass('input-ghost') ) {
        var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
        element.attr("name",$(this).attr("name"));
        element.change(function(){
          element.next(element).find('input').val((element.val()).split('\\').pop());
          ActivateSaveButton();
        });
        $(this).find("button.btn-choose").click(function(){
          element.click();
          ActivateSaveButton();
        });
        $(this).find("button.btn-reset").click(function(){
          element.val(null);
          $(this).parents(".input-file").find('input').val('');
          ActivateSaveButton();
        });
        $(this).find('input').css("cursor","pointer");
        $(this).find('input').mousedown(function() {
          $(this).parents('.input-file').prev().click();
          ActivateSaveButton();
          return false;
        });
        return element;
      }
    }
  );
};

//Activer ou désactiver le bouton enregistrer
function ActivateSaveButton(){
  var file = $("#id_fichier_bordereau").val();
  if (file) {
    $("#id_submit").prop('disabled', false);
  } else {
    $("#id_submit").prop('disabled', true);
  }
}

$(function() {
  bs_input_file();
  ActivateSaveButton();
});