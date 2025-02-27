function togglePlayPause() {
  let video = document.getElementById("back_video");
  let playPauseImg = document.getElementById("playPauseImg");

  if (video.paused || video.ended) {
    video.play();
    playPauseImg.src =
      "/home/volodymyrkyba/work/sport_ai/frontend/static/images/pause.png";
  } else {
    video.pause();
    playPauseImg.src =
      "/home/volodymyrkyba/work/sport_ai/frontend/static/images/play-button.png";
  }
}
