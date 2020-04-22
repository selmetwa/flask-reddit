let postTitle;
  let postContent;
  postTitle = document.querySelector(".create-post-title");
  postContent = document.querySelector(".create-post-content");
  function empty() {
      if (postTitle.value == "" && postContent.value == "") {
          alert("fields cannot be empty");
          postTitle.classList.add('error')
          postContent.classList.add('error')
          return false;
      }
      else if (postTitle.value == "") {
          alert("post title cannot be empty");
          postTitle.classList.add('error')
          return false;
      }
      else if (postContent.value == "") {
          alert("post text cannot be empty");
          postContent.classList.add('error')
          return false;
      };
  }

  function isValidURL(string) {
    console.log('string: ', string)
    var res = string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    console.log('res: ', res)
    return (res !== null)
  };

  let linkContent = document.querySelector('.link-input')
  let formLinkPostContent = document.querySelector('.post-title-form-link')
  function empty_link() {
    if (linkContent.value == "" && formLinkPostContent.value == "") {
      linkContent.classList.add('error')
      formLinkPostContent.classList.add('error')
      alert("fields cannot be empty");
      return false
    }
    else if (formLinkPostContent.value == "") {
      alert("post title cannot be empty");
      formLinkPostContent.classList.add('error')
      return false;
    }
    else if (!isValidURL(linkContent.value)) {
      alert("must be valid url");
      linkContent.classList.add('error')
      return false;
    }
    
  }
  let formLinkButton = document.querySelector('.link-tab')
  let formTextButton = document.querySelector('.text-tab')

  let formLink = document.getElementById('form-link');
  let formText = document.getElementById('form-text');

  formLinkButton.addEventListener('click', () => {
    formLink.style.display = 'flex'
    formText.style.display = 'none'
    formLinkButton.classList.add('active')
    formTextButton.classList.remove('active')
  })

  formTextButton.addEventListener('click', () => {
    formLink.style.display = 'none'
    formText.style.display = 'flex'
    formLinkButton.classList.remove('active')
    formTextButton.classList.add('active')
  })
