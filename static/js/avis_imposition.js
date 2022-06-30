//Gestion des taxes
function ai_OnTaxeChanged(){
    var selectedValue = $('#id_taxe').val()
    var copie = $('#id_nombre_copie').val()
    
    if (selectedValue != "") {
    	$.ajax({
            url : '/finance/avis_imposition/helpers/taxe_changed/', //"{% url avis_imposition_taxe_changed %}"
            type : "POST",
            data : {"taxe" : selectedValue},
            dataType : "json",
            success : function(data){
                //Afficher le montant de la taxe            
                $('#id_taxe_montant').val(data.taxe_montant);
                $('#id_montant_total').val(data.taxe_montant * copie);

                $('#id_libelle').val(data.libelle);
            }
        });
    } else { $('#id_libelle').val(''); }
}

//Gestion des montants
function ai_OnCoastChanged(){
    var copie = $('#id_nombre_copie').val()
    var tarif = $('#id_taxe_montant').val()
    $('#id_montant_total').val(tarif * copie);
}
