import { useCookies } from "vue3-cookies"

interface Data {
  method?: 'GET' | 'POST'
  body?: {
    [key: string]: any
  }
}

const { cookies } = useCookies()

export const useFetch = async (url: string, data?: Data) => {
  const headers: { [key: string]: string } = {}
  const authToken = cookies.get("authToken")
  if (authToken) {
    headers["Auth-Token"] = authToken
  }

  const res = await fetch(`${import.meta.env.VITE_API_URL}/${url}/`, {
    method: data?.method || 'GET',
    body: JSON.stringify(data?.body),
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  })

  return {
    status: res.status,
    data: await res.json()
  }
}
