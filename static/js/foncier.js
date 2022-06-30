//------------------------------------------------------------------------
//----------- RECHERCHE DES ACCESSIBILITE D'UNE PARCELLE PRIVÉE ----------
//------------------------------------------------------------------------

function Load_Accessibilite(){  
  var selectedValue = $('#id_parcelle').val();
  
  if(selectedValue != null && selectedValue != "") {
    var impot_non_batie_id = $('#impot_non_batie_id').val()
    
    $.ajax({
      url : "/foncier/parcelle/load_impot/", //View: mod_foncier.load_impot_by_accessibilite
      type : "POST",
      data : {"id_parcelle" : selectedValue},
      dataType : "json",
      success : function(data){
        if(data.success)
        {         
          //Load dropdown
          Helpers.BuildDropdown(data.impots, $('#id_impot_non_batie'), '--------', impot_non_batie_id, "tnb_categorie__nom", 'impot');
        }
        else {
          // console.log("not success!!")
        }
      }
    });  
  } 
}

//---------------------------------------------
function Manage_Accessibilite() {
  /*
  Gérer l'accessibilité par rappot à la rue et avenue
  Si accebilité appratient à la rue alors on desactive l'accessibilité
  **/

  var id_numero_rueavenue = $('#id_numero_rueavenue').val();
  if(id_numero_rueavenue != null && id_numero_rueavenue != "") {
    var id_accessibilite = $('#id_accessibilite').val();
    $.ajax({
      url : "/parametrage/adresse/rue_avenue/load_accesibilite/", //View: mod_parametrage.load_accessibilite_by_rue_avenue
      type : "POST",
      data : {"id_numero_rueavenue" : id_numero_rueavenue},
      dataType : "json",
      success : function(data){
        if(data.success)
        {
          //alert($("#id_numero_rueavenue").is('[disabled]'));

        
          /*
          if ($('#id_numero_police').is(":disabled")==false) {
            $('#id_accessibilite').addClass("disabled-element");
          } else { alert(1); }*/
        }
        else {
          //$('#id_accessibilite').removeClass("disabled-element");
        }
      }
    });  
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