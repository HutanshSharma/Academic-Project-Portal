document.querySelectorAll('.switch-form').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        document.querySelectorAll('.form').forEach(form => {
            form.classList.remove('active');
        });
        document.getElementById(targetId).classList.add('active');
    });
});
var a = document.querySelector(".submit-btn");
a.addEventListener('click', () => {
    const email = document.querySelector('#signin-email').value;
    const password = document.querySelector('#signin-password').value;

    if (email === "hutansh@gmail.com" && password === "1234") {
        window.location.href = "index.html";
    } else {
        alert("Invalid email or password!");
    }
});

