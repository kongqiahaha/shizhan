var page5 = new Vue({
  el: ".head",
  data: {
    user_inf: {
      csrfmiddlewaretoken: "{{csrf_token}}",
      us_name: "",
      password_1: "",
      email: "",
      picked: "",
      job_title: "0",
    },
    password_2: "",
    error: "",
    isError: false,
    enterPW: "请再次输入密码：",
  },
  methods: {
    errorF: function () {
      if (this.user_inf.password_1 !== "" && this.password_2 !== "") {
        if (this.user_inf.password_1 != this.password_2) {
          this.isError = true;
        }
        if (this.user_inf.password_1 === this.password_2) {
          this.isError = false;
        }
      } else {
        this.isError = false;
      }
      console.log(this.isError);
      this.error = this.isError ? "has-error" : "";
    },
    to_search:function(){
      console.log("1111")
    },
    registered: function () {
      console.log(JSON.stringify(this.user_inf));
      if (
        this.user_inf.password_1 === "" ||
        this.user_inf.us_name === "" ||
        this.user_inf.email === "" ||
        this.user_inf.picked === "" ||
        this.isError
      ) {
        alert("填写的信息不完善或信息有误，请检查后重试！");
      } else {
        if (!this.isError) {
          axios
            .post("sign_up", this.user_inf)
            .then(function (response) {
              console.log(response.data.code);
              if (response.data.code === 200) {
                alert("注册失败，可能该用户名已存在！");
              } else {
                alert("注册成功！即将跳转到登陆页面！");
                  location.href=("/page3");
              }
            })
            .catch(function (err) {
              console.log(err);
            });
        }
      }
    },
  },
});

