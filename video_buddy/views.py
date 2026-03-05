import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import FavouriteVideo

# ── YouTube search using youtubesearchpython (no API key needed) ─────────────
def _search_youtube(query, max_results=6):
    """Return a list of video dicts [{title, url, thumbnail, channel, duration}]"""
    try:
        from youtubesearchpython import VideosSearch
        vs = VideosSearch(query + " tutorial explained", limit=max_results)
        raw = vs.result().get("result", [])
        videos = []
        for item in raw:
            thumb = ""
            if item.get("thumbnails"):
                thumb = item["thumbnails"][0].get("url", "")
            duration = ""
            if item.get("duration"):
                duration = item["duration"]
            videos.append({
                "title":    item.get("title", "Untitled"),
                "url":      item.get("link", ""),
                "thumbnail": thumb,
                "channel":  item.get("channel", {}).get("name", ""),
                "duration": duration,
                "views":    item.get("viewCount", {}).get("short", ""),
            })
        return videos
    except Exception as e:
        return []


# ── Main Video Buddy page ─────────────────────────────────────────────────────
@login_required
def video_buddy_home(request):
    favourites = FavouriteVideo.objects.filter(user=request.user)
    return render(request, "video_buddy/video_buddy.html", {
        "favourites": favourites,
    })


# ── AJAX: search YouTube ──────────────────────────────────────────────────────
@login_required
def search_videos(request):
    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"status": "error", "message": "Query is empty."}, status=400)

    videos = _search_youtube(query)
    return JsonResponse({"status": "success", "videos": videos})


# ── AJAX: save a favourite ────────────────────────────────────────────────────
@login_required
@require_POST
def save_favourite(request):
    try:
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        url  = data.get("url",  "").strip()
    except (json.JSONDecodeError, KeyError):
        name = request.POST.get("name", "").strip()
        url  = request.POST.get("url",  "").strip()

    if not name or not url:
        return JsonResponse({"status": "error", "message": "Name and URL are required."}, status=400)

    fav = FavouriteVideo.objects.create(user=request.user, name=name, url=url)
    return JsonResponse({
        "status": "success",
        "id":     fav.id,
        "name":   fav.name,
        "url":    fav.url,
    })


# ── AJAX: edit a favourite ────────────────────────────────────────────────────
@login_required
@require_POST
def edit_favourite(request, pk):
    fav = get_object_or_404(FavouriteVideo, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        name = data.get("name", "").strip()
        url  = data.get("url",  "").strip()
    except (json.JSONDecodeError, KeyError):
        name = request.POST.get("name", "").strip()
        url  = request.POST.get("url",  "").strip()

    if not name or not url:
        return JsonResponse({"status": "error", "message": "Name and URL are required."}, status=400)

    fav.name = name
    fav.url  = url
    fav.save()
    return JsonResponse({"status": "success", "name": fav.name, "url": fav.url})


# ── AJAX: delete a favourite ──────────────────────────────────────────────────
@login_required
@require_POST
def delete_favourite(request, pk):
    fav = get_object_or_404(FavouriteVideo, pk=pk, user=request.user)
    fav.delete()
    return JsonResponse({"status": "success"})
