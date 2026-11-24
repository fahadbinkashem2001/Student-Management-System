    setTimeout(function(){
        const successMessages = document.querySelectorAll(".success-message");
        successMessages.forEach(function(message){
            message.style.opacity = "0";
            setTimeout(function(){
                message.remove();
            },500);
        });
    },2000);