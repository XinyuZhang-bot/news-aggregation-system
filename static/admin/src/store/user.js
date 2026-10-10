export default {
  state() {
    return {
      "user_id": 0,
      "token": "",
      "username": "",
      "referee_id": 0,
      "vip": 0,
      "gm": 0,
      "mc": 0,
      "phone": "",
      "phone_state": 0,
      "email": "",
      "email_state": 0,
      "login_ip": "",
      "login_time": "",
      "user_group": "",
      "user_admin": "",
      "signature": "",
      "nickname": "",
      "avatar": "/img/avatar.png",
      "invite_code": "",
      "friends": "",
      "state": 0
    }
  },
  mutations: {
    user_set(state, obj) {
      for (var k in obj) {
        state[k] = obj[k]
      }
      if (obj.token) {
        $.db.set("token", obj.token, 120);
      }
    },
    quit(state) {
      state.user_id = 0;
      state.token = "";
      state.username = "";
      state.referee_id = 0;
      state.vip = 0;
      state.gm = 0;
      state.mc = 0;
      state.phone = "";
      state.phone_state = 0;
      state.email = "";
      state.email_state = 0;
      state.login_ip = "";
      state.login_time = "";
      state.user_group = "";
      state.user_admin = "";
      state.signature = "";
      state.nickname = "";
      state.avatar = "/img/avatar.png";
      state.invite_code = "";
      state.friends = "";
      state.state = 0;
      $.db.del("token");
    }
  }
}
