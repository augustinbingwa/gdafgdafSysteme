//---------------------------------------------------------
// TANSPORT - VEHICULE - GESTION CATEGORIE et COMPTE PROPRE
//---------------------------------------------------------
function OnCategorieChanged(){
	// Identifiant de la sous catégorie seléctionnée
    var id = $('#id_sous_categorie').val();
    
    $.ajax({
	    url : '/transport/vehicule/sous_categorie/',
	    type : "POST",
	    data : {"id" : id},
	    dataType : "json",
	    success : function(data){
	     	if (data.has_compte_propre) {
	     		//Activer compte propre et mettre 'NON' sa valeur
	     		$('#id_compte_propre').attr("disabled", false);
	     		$('#id_compte_propre').val('False');
	     	} else {
	     		// Désactiver compte propre et Mettre 'NON' sa valuer
	     		$('#id_compte_propre').attr("disabled", true);
	     		$('#id_compte_propre').val('False');
	     	}
	    },
	 });
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