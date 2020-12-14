var form = new Vue({
  el: "#login",
  data: {
    login_inf: {
      user_name: "",
      password: "",
      is_remember: false,
    },
  },
  methods: {
    login: function () {
      console.log(this.login_inf);
      axios
        .post("login", this.login_inf)
        .then(function (response) {
          console.log(response.data.code);
          if (response.data.code === 200) {
            alert("用户名或密码输入错误，请重新输入！");
          } else {
            location.href = "/page3";
          }
        })
        .catch(function (err) {
          console.log(err);
        });
    },
  },
});
