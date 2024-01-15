import {axiosRequest} from "./axiosHelper";

const BASEURL = '' // config ENV

/**
 *
 * @param {string} url
 * @param {object} data
 * @param {string} method
 * @param {object} params
 * @return {Promise<axios.AxiosResponse<*>>|*}
 */
export default function fetchAuthenticatedApi({url,data ={},method = 'GET',params= null}){
    const token = '' // select store redux
    return axiosRequest(
        {
            url: BASEURL +url,
            method,
            token,
            params,
            data
        }
    );

}