var app = new Vue({
  el: '#app',
  data: {
    user: null,
    users: null,
    tasks: null,
    message: 'Hello Vue!'
  },
  computed: {
  },
  methods: {
    statusstr: function (v) {
      switch (v) {
        case 0: return "-";
        case 1: return "Executing";
        case 2: return "Done";
        default: return "";
      }
    },
    datestr: function (ts) {
      if (!ts) return "-";
      var pad = function (v) {
        return v < 10 ? '0' + v : v;
      }
      var d = new Date( ts * 1000 );
      var year = d.getFullYear();
      var month = pad(d.getMonth() + 1);
      var day = pad(d.getDate());
      var hour = pad(d.getHours());
      var min = pad(d.getMinutes());
      var sec = pad(d.getSeconds());
      return year + '-' + month + '-' + day + ' ' + hour + ':' + min + ':' + sec;
    },
    login: function () {
      console.log("login");
      var provider = new firebase.auth.GoogleAuthProvider();
      //firebase.auth().signInWithRedirect(provider);
      firebase.auth().signInWithPopup(provider);
    },
    logout: function () {
      console.log("logout");
      firebase.auth().signOut();
    },
    request: function () {
      console.log("request");
      var users = this.users;
      var user = this.user;
      var email = user.email;
      var server = users[email].server;
      user.getIdToken(/* forceRefresh */ true)
      .then(function(idToken) {
        return fetch("/request", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "email": email,
            "server": server,
            "idtoken": idToken,
          })
        });
      }).then((result) => {
        console.log(result)
      }).catch(function(error) {
        console.log(error)
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
var usersRef = firebase.database().ref('users');
var tasksRef = firebase.database().ref('tasks');

usersRef.on('value', function(snapshot) {
  var users = {}
  snapshot.val().forEach(row => { users[row.email] = row; })
  app.users = users;
});

tasksRef.on('value', function(snapshot) {
  app.tasks = snapshot.val();
});
