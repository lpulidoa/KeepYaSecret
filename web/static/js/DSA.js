function exp_mod(a, b, c) {
    var x = 1;
    var y = a;
    for (var i = 0; i < b; i++) {
      x = (x * a) % c;
    }
    return x;
  }
  
  function Sig_1(x, k, p, q, alpha, a) {
    var beta = exp_mod(alpha, a, p);
    var gamma = (exp_mod(alpha, k, p)) % q;
    var delta = ((x + a * gamma) * exp_mod(k, q - 2, q)) % q;
    return [gamma, delta]; 
  }
  
  function Ver(x, gamma, p, q, delta, alpha, beta) {
    var inv_delta = exp_mod(delta, q - 2, q);
    var e_1 = (x * inv_delta) % q;
    var e_2 = (gamma * inv_delta) % q;
  
    if (((exp_mod(alpha, e_1, p) * exp_mod(beta, e_2, p)) % p) % q == gamma) {
      return "Successful authentication";
    } else {
      return "Sorry, authentication has failed";
    }
  }
  
  var g=7879
  var y=101
  
  var Xhita = 170
  var Xhita_1 = 4567
  var a_0 = 75
  
  //console.log(Sig_1(mssage, keyes, g, y, Xhita, a_0 ))
  
  //console.log(Ver(mssage, r1, g, y, r2, Xhita, Xhita_1))
  
  

  document.getElementById('Signing').onclick = function() {

   var Mss = document.getElementById("Message").value
   var Key = document.getElementById("Key").value

   var outputText = Sig_1(Mss, Key, g, y, Xhita, a_0 )

   document.getElementById("Digital Sign").value = outputText

  }
  
  document.getElementById('verification').onclick = function() {
    var Mss = document.getElementById("Message").value
    var Gamma = document.getElementById("Gamma").value
    var Delta = document.getElementById("Delta").value

    var outputText = Ver(Mss, Gamma, g, y, Delta, Xhita, Xhita_1)
    document.getElementById("verification_output").value = outputText
  }
