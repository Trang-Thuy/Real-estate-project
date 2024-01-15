import {useEffect, useState} from 'react';
import fetchAuthenticatedApi from "../helpers/fetchAuthenticatedApi";
import isEmpty from "../helpers/utils/isEmpty";

/**
 * useFetchApi hook for fetch data from api with url
 *
 * @param url
 * @param defaultData
 * @param {*} presentDataFunc
 * @param initLoad
 * @param method
 * @param postData
 * @returns {{setTotal: (value: (((prevState: number) => number) | number)) => void, setPagination: (value: (((prevState: {}) => {}) | {})) => void, pagination: {}, data: *[], setData: (value: (((prevState: *[]) => *[]) | *[])) => void, refetch: ((function(*): Promise<undefined|*>)|*), loading: boolean, setErrors: (value: (((prevState: *[]) => *[]) | *[])) => void, handleChangeInput: (function(*, *): void), total: number, setLoading: (value: (((prevState: boolean) => boolean) | boolean)) => void, errors: *[], fetched: boolean}}
 */
export default function useFetchApi(
  url,
  defaultData = [],
  presentDataFunc = null,
  initLoad = true,
  method = 'GET',
  postData = {}
) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(defaultData);
  const [pagination, setPagination] = useState({});
  const [errors, setErrors] = useState([]);
  const [fetched, setFetched] = useState(false);
  const [total, setTotal] = useState(0);
  const [pageInfo, setPageInfo] = useState({});

  const handleApi = async (url, postData, method) => {
    try {
      setLoading(true);
      const resp =
          method === 'GET'
              ? await fetchAuthenticatedApi(url)
              : await fetchAuthenticatedApi(url, postData, method);
      if (resp.data) {
        const newData = presentDataFunc ? presentDataFunc(resp.data) : resp.data;
        if (!isEmpty(defaultData)) {
          setData(prev => ({...prev, ...newData}));
        } else {
          setData(newData);
        }
      }
      if (resp.pageInfo) setPageInfo(resp.pageInfo);
      if (resp.pagination) {
        const pagination = resp.pagination;
        setPagination(pagination);
        if (Object.hasOwn(pagination, 'total')) setTotal(pagination.total);
      }
      if (resp.errors) setErrors([...errors, resp.errors]);
    } catch (e) {
      console.log(e);
      setErrors([...errors, e.message]);
    } finally {
      setLoading(false);
      setFetched(true);
    }

  }
  async function fetchApi() {
    if (url === '') return;
    await handleApi(url, postData, method)
  }

  async function refetch(reFetchUrl = url, reFetchBody = postData) {
    if (reFetchUrl === '') return;
    await handleApi(reFetchUrl, reFetchBody, method)
  }

  useEffect(() => {
    if (initLoad && !fetched) {
      fetchApi().then(() => {});
    }
  }, []);

  const handleChangeInput = (key, value) => setData(prev => ({...prev, [key]: value}));

  return {
    loading,
    data,
    setData,
    total,
    setTotal,
    pagination,
    setPagination,
    refetch,
    errors,
    setLoading,
    fetched,
    setErrors,
    handleChangeInput,
    pageInfo
  };
}
