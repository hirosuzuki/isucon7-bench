var app = new Vue({
  el: '#app',
  data: {
    user: null,
    message: 'Hello Vue!'
  },
  methods: {
    login: function () {
      console.log("doSomething");
      var provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
    }
  }
});

var user = firebase.auth().currentUser;
console.log("User=" + user)

firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    console.log("Logined: " + user.email)
    app.user = user.email
    // User is signed in.
  } else {
    console.log("No Login:")
    app.user = null
    // No user is signed in.
  }
});

firebase.auth().getRedirectResult().then(function(result) {
  if (result.credential) {
    // This gives you a Google Access Token. You can use it to access the Google API.
    var token = result.credential.accessToken;
  }
  var user = result.user;
  console.log(result);
  console.log("getRedirect Success " + user)
}).catch(function(error) {
  console.log("getRedirect Fail " + error.message)
});