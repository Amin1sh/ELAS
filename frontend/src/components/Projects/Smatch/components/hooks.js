import {useEffect, useState} from 'react';
import userToken from "./userContext";

const API_URL = process.env.REACT_APP_BASE_URL + '/smatch/';

export function useAPIGet(path) {
    const [ response, setResponse ] = useState();

    const refresh = async () => {
        const resp = await fetch(`${API_URL}${path}`, {
        headers: userToken ? { "Authorization": `Bearer ${userToken}` } : {}
        });

        setResponse(resp);
    }

    useEffect(async () => {
        await refresh();
    }, [userToken, path]);

    return { response, refresh };
}

export function useAPIPost(path) {
    const sendRequest = async (data) => {
        const resp = await fetch(`${API_URL}${path}`, {
        method: "POST",
        body: JSON.stringify(data),
        headers: { "Content-Type": "application/json", ...(userToken ? { "Authorization": `Bearer ${userToken}` } : {}) }
        });

        return resp;
    }

    return sendRequest;
}

export function useAPIJson(data) {
    const [ jsonData, setJsonData ] = useState();

    useEffect(async () => {
    if (data) {
        if (!data.bodyUsed) {
        setJsonData(await data.json());
        }
    } else {
        setJsonData(undefined);
    }
    }, [data]);

    return { jsonData };
}

export function useTopics() {
    const { response } = useAPIGet("topics");
    const { jsonData } = useAPIJson(response);

    return jsonData;
}

export function useSendSwipedTerms() {
    const sendRequest = useAPIPost("swiped_terms");

    return sendRequest;
}

export function useGenerateClusters() {
    const sendRequest = useAPIPost("generate_clusters");

    return sendRequest;
}

export function useUserCount() {
    const { response } = useAPIGet("user_count");
    const { jsonData } = useAPIJson(response);

    return jsonData;
}

export function useThreads() {
    const { response } = useAPIGet("threads");
    const { jsonData } = useAPIJson(response);

    return jsonData;
}

export function useCreateThread() {
    const sendRequest = useAPIPost("threads");

    return sendRequest;
}

export function useThread(id) {
    const { response, refresh } = useAPIGet(`threads/${id}`);
    const { jsonData } = useAPIJson(response);

    return { thread: jsonData, refresh };
}
  
export function useCreateReply(thread_id) {
    const sendRequest = useAPIPost(`threads/${thread_id}/replies`);

    return sendRequest;
}

export function useStoreSuggestion() {
    const sendRequest = useAPIPost("store_suggestion");

    return sendRequest;
}

export function useGetHistory() {
    const { response } = useAPIGet("get_history");
    const { jsonData } = useAPIJson(response);

    return jsonData;
}

export function useCourse(id) {
    const { response, refresh } = useAPIGet(`course/${id}`);
    const { jsonData } = useAPIJson(response);

    return jsonData;
}