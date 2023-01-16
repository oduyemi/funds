function smDevice(sm){
    if (sm.matches){
        document.body.style.backgroundColor="#0e34a0";
        document.getElementById('logo').src="images/logo/logo_white.png"
        document.getElementById("sm_msg").innerHTML=document.getElementById('_intro_msg').innerHTML
    }
}

var sm=window.matchMedia('(max-width:700px)');
    smDevice(sm);

$(document).ready(function(){
    $("#invest_group").hide();
    $(".ctabtn").hide();


    $("#invest_type").click(function(){
        var invest=$("#invest_type").children("option:selected").val();
        if(invest=="raise_fund"){
           $("#invest_type").hide();
           $("._dropdown").text("I am...")
           $("#invest_group").show();
           $("#ctabtn_ctd").show();
        }
    });
    $("#ctabtn_ctd").click(function(){
        var investType=$("#invest_group").children("option:selected").val();
        if(investType=="ngo"){window.location.href="ngo.html"}
        if(investType=="prestartup"){window.location.href="prestartup.html"}
        if(investType=="startup"){window.location.href="startup.html"}
        if(investType=="smb"){window.location.href="smb.html"}
        if(investType==""){alert("Choose an option")}
    });
});
