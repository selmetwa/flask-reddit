let form = document.querySelector('.addPostForm')
console.log('form: ', form)
document.querySelector('.showForm').addEventListener('click', () => {
    console.log('form: ', form)
    form.style.display = "flex"
})