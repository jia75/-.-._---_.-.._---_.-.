curmode="choice"
colorone=""
colortwo=""
let last = 0
function swap() {
    if (curmode == "rank") {
        document.getElementById("choice-page").style.display = "block"
        document.getElementById("rank-page").style.display = "none"
        curmode="choice"
    } else {
        document.getElementById("choice-page").style.display = "none"
        document.getElementById("rank-page").style.display = "block"
        curmode="rank"
    }
}
async function choose(the) {
    const now = Date.now()
    if (now - last < 500) return
    last = now
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 5000) // 5s
    try {
        const result = await fetch('/api/say-result', {
            method: 'POST',
            headers: { 'content-type': 'text/plain' },
            body: colorone+" "+colortwo+" "+the,
            signal: controller.signal,
            credentials: 'include' // send cookies if needed
        })
        clearTimeout(timeout)
        if (!result.ok) throw new Error(await result)
        console.log(result)
    } catch (err) {
        if (err.name === 'AbortError') console.warn('request timed out')
        else console.error('fetch error', err)
    }
    getcolors()
}
async function getcolors() {
    const res = await fetch('/api/get-colors-to-grade')
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText)
    const data = await res.text()

    ent = data.split(" ")

    colorone = ent[0]
    colortwo = ent[1]

    document.getElementById("coll-one").style.backgroundColor = "#"+colorone
    document.getElementById("coll-two").style.backgroundColor = "#"+colortwo
}
async function getleaderboard() {
    const res = await fetch('/api/send-leaderboard')
    if (!res.ok) throw new Error(res.status + ' ' + res.statusText)
    const data = await res.text()
    for (let i = 0; i< 64;++i) {
        document.getElementById("colornew-"+i).style.backgroundColor = "#"+data.slice(3*i,3*i+3)
    }
}
