//-----------------------------------------------
// ACTIVITE - STANDARD - GESTION TYPE D'ESPACE
//-----------------------------------------------
function OnTypeEspaceChanged(){
    var selectedValue = $('#id_type_espace').val();
    if(selectedValue == 1) //enum PUBLIQUE=1
    {
        //Réactiver espace publique
        $('#id_auto_allocation_espace_publique').attr("disabled", false); 

        //Désactiver le contribuable et les adresses (Quartier - RueAvenue)        
        $('#id_auto_contribuable').attr("disabled", true);
        $('#id_auto_adresse').attr("disabled", true);
        $('#id_auto_numero_rueavenue').attr("disabled", true);
        $('#id_numero_police').attr("disabled", true);

        //Initialiser les valeurs
        $('#id_numero_police').val('');

        //Gestion des champs required
        $('#allocation_required').css("display", "inline"); 
        $('#contribuable_required').css("display", "none"); 
        $('#adresse_required').css("display", "none"); 
        $('#numero_rueavenue_required').css("display", "none"); 
    } else {
        //Désactiver espace publique
        $('#id_auto_allocation_espace_publique').attr("disabled", true); 

        //Reactiver le contribuable et les adresses (Quartier - RueAvenue)
        $('#id_auto_contribuable').attr("disabled", false); 
        $('#id_auto_adresse').attr("disabled", false); 
        $('#id_auto_numero_rueavenue').attr("disabled", false);
        $('#id_numero_police').attr("disabled", false);
        
        //Initialiser les valeur
        $('#id_auto_allocation_espace_publique').val('');
        $('#id_allocation_espace_publique').val(''); //Hidden field

        //Gestion des champs required
        $('#allocation_required').css("display", "none"); 
        $('#contribuable_required').css("display", "inline"); 
        $('#adresse_required').css("display", "inline"); 
        $('#numero_rueavenue_required').css("display", "inline"); 
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