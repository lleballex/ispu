import { useCookies } from "vue3-cookies"

interface Data {
  method?: "GET" | "POST" | "DELETE" | "PUT"
  body?: {
    [key: string]: any
  }
  params?: {
    [key: string]: string
  }
}

const { cookies } = useCookies()

export const useFetch = async <IData>(url: string, data?: Data) => {
  const headers: { [key: string]: string } = {}
  const authToken = cookies.get("authToken")
  if (authToken) {
    headers["Auth-Token"] = authToken
  }

  let params = ""

  if (data?.params) {
    Object.keys(data.params).forEach((param) => {
      if (data.params?.[param]) {
        !params ? (params = "?") : (params += "&")
        params += `${param}=${data.params[param]}`
      }
    })
  }

  const res = await fetch(`${import.meta.env.VITE_API_URL}/${url}/${params}`, {
    method: data?.method || "GET",
    body: JSON.stringify(data?.body),
    headers: {
      ...headers,
      "Content-Type": "application/json",
    },
  })

  let jsonData
  try {
    jsonData = await res.json()
  } catch (e) {}

  return {
    status: res.status,
    data: (jsonData || null) as IData | null,
  }
}
