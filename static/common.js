
function e() {
firebase.auth().signInWithEmailAndPassword(email, password).catch(function(error) {
  // Handle Errors here.
  var errorCode = error.code;
  var errorMessage = error.message;
  // ...
});
};

var provider = new firebase.auth.GoogleAuthProvider();

document.querySelector("#login-button").addEventListener("click", function () {
  firebase.auth().signInWithRedirect(provider);
});

document.querySelector("#logout-button").addEventListener("click", function () {
  firebase.auth().signOut();
});

document.querySelector("#login-button").style.display = "none";
document.querySelector("#logout-button").style.display = "none";

// https://firebase.google.com/docs/auth/web/google-signin?authuser=1

var U;

firebase.auth().onAuthStateChanged(function(user) {
  document.querySelector("#login-button").style.display = "none";
  document.querySelector("#logout-button").style.display = "none";
  if (user) {
    U = user;
    console.log("Signed in: " + user.email);
    // User is signed in.
    var displayName = user.displayName;
    var email = user.email;
    var emailVerified = user.emailVerified;
    var photoURL = user.photoURL;
    var isAnonymous = user.isAnonymous;
    var uid = user.uid;
    var providerData = user.providerData;
    document.querySelector("#logout-button").style.display = "";
  } else {
    console.log("Signed out");
    document.querySelector("#login-button").style.display = "";
  }
});

var database = firebase.database();

document.querySelector("#request-button").addEventListener("click", function () {
  var newPostKey = firebase.database().ref().child('tasks').push().key;
  console.log("Request: " + newPostKey);
  var updates = {};
  var now = (new Date()).getTime();
  updates['/tasks/' + newPostKey] = {
    "jobid": 0,
    "who": "suzuki",
    "target": "A",
    "score": null,
    "createat": now,
  };
  firebase.database().ref().update(updates);
});

document.querySelector("#request2-button").addEventListener("click", function () {
  firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(idToken) {
    console.log("idToken: " + idToken);
    fetch("/req", {
      method: "POST",
      headers: {
        "X-ID-TOKEN": idToken,
      }
    });
    console.log("...");
    // Send token to your backend via HTTPS
    // ...
  }).catch(function(error) {
    // Handle error
  });
});
