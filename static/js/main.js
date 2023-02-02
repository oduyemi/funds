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
        if(investType=="ngo"){window.location.href="/ngo"}
        if(investType=="prestartup"){window.location.href="/prestart"}
        if(investType=="startup"){window.location.href="/startup"}
        if(investType==""){alert("Choose an option")}
    });

    $('.login').click(function(){
        window.location.href = '/login';
    });

    $('.signup').click(function(){
        window.location.href = '/signup';
    });
});
