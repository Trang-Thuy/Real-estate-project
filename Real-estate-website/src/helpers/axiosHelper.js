import axios from 'axios';

export const axiosMethod = {
    GET: 'GET',
    POST: 'POST',
    PUT: 'PUT',
    DELETE: 'DELETE',
};


/**
 *
 * @param url
 * @param method
 * @param token
 * @param params
 * @param data
 * @return {Promise<axios.AxiosResponse<any>> | *}
 */
export const axiosRequest = (
    {
        url,
        method = axiosMethod.GET,
        token = '',
        params = null,
        data = null
    }
) => {
    const axiosConfig = {
        url,
        method,
        headers: {},
        params,
    };

    if (token) {
        axiosConfig.headers.Authorization = `Bearer ${token}`;
    }
    axiosConfig.data = data;
    return axios(axiosConfig);
};
