var app = new Vue({
  el: '#app',
  data: {
    user: null,
    tasks: null,
    message: 'Hello Vue!'
  },
  methods: {
    login: function () {
      console.log("login");
      var provider = new firebase.auth.GoogleAuthProvider();
      firebase.auth().signInWithRedirect(provider);
    },
    logout: function () {
      console.log("logout");
      firebase.auth().signOut();
    },
    request: function () {
      console.log("request");
      fetch("/request", {
        method: "POST"
      });
    }
  }
});

firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    app.user = user;
  } else {
    app.user = null;
  }
});

var database = firebase.database();
var tasksRef = firebase.database().ref('tasks');

tasksRef.on('value', function(snapshot) {
  app.tasks = snapshot.val();
});
