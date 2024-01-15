import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import {axiosMethod, axiosRequest} from "../helpers/axiosHelper";
const BASEURL = '' // config ENV

const authSlice = createSlice({
   name: 'auth',
   initialState: {
      isLogin: false,
      user: null,
      status: 'idle',
      message: null,
      token: null,
   },
   reducers: {
      logout: (state) => {
         state.isLogin = false;
         state.user = null;
         state.status = null;
      },
   },
   extraReducers: (builder) => {
      builder.addCase(login.pending, (state, action) => {
         state.status = 'ld';
         state.isLogin = false;
      });
      builder.addCase(login.fulfilled, (state, action) => {
         state.isLogin = true;
         state.user = action.payload.data;
         state.token = action.payload.token;
         state.status = 'idle';
      });
      builder.addCase(login.rejected, (state, action) => {
         state.isLogin = false;
         state.status = 'error';
         state.message = action.payload;
      });
      builder.addCase(register.pending, (state, action) => {
         state.status = 'ld';
         state.isLogin = false;
      });
      builder.addCase(register.fulfilled, (state, action) => {
        state.isLogin = true;
        state.user = action.payload.data;
        state.token = action.payload.token;
        state.status = 'idle';
      });
      builder.addCase(register.rejected, (state, action) => {
         state.status = 'idle';
         state.message = action.payload;
      });
   },
});

export default authSlice;

export const login = createAsyncThunk(
   'auth/login',
   async (data, { rejectWithValue }) => {
      try {
         const res = await axiosRequest(
             {
                url: BASEURL +'/login',
                method:axiosMethod.POST,
                data
             }
         );
         console.log(res);
         return res.data;
      } catch (e) {
         console.log('[login]' + e.response.data);
         return rejectWithValue(e.response.data);
      }
   }
);

export const register = createAsyncThunk(
   'auth/register',
   async (data, { rejectWithValue }) => {
      try {
         const res =  await axiosRequest(
             {
                url: BASEURL +'/register',
                method:axiosMethod.POST,
                data
             });
         console.log(res);
         return res.data;
      } catch (e) {
         console.log('[register]' + e.response.data);
         return rejectWithValue(e.response.data);
      }
   }
);
