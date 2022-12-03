import axios from "axios";

export const SD_API = axios.create({
  baseURL: `http://0.0.0.0:8002/`
});

export const MU_API = axios.create({
  baseURL: `http://0.0.0.0:8003/`
});




const getCurrentUser = () => {

  const user = localStorage.getItem("user")
  return JSON.parse(user);

};

const AuthService = {
  SD_API,
  MU_API,
  getCurrentUser,
}

export default AuthService;
