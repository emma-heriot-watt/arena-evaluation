import { Signaling, WebSocketSignaling } from "./signaling.js";
import Peer from "./peer.js";
import * as Logger from "./logger.js";

function uuid4() {
  var temp_url = URL.createObjectURL(new Blob());
  var uuid = temp_url.toString();
  URL.revokeObjectURL(temp_url);
  return uuid.split(/[:/]/g).pop().toLowerCase(); // remove prefixes
}

export class VideoPlayer {
  constructor(element) {
    const _this = this;
    this.pc = null;
    this.channel = null;
    this.connectionId = null;

    this.localStream = new MediaStream();
    this.video = element;
    this.video.setAttribute("muted", "true");
    this.video.playsInline = true;
    this.video.addEventListener(
      "loadedmetadata",
      function () {
        _this.video.play();
        _this.resizeVideo();
      },
      true,
    );
    this.ondisconnect = function () {
      console.log("Disconnected");
    };
  }

  async setupConnection(useWebSocket) {
    const _this = this;

    // close current RTCPeerConnection
    if (this.pc) {
      Logger.log("Close current PeerConnection");
      this.pc.close();
      this.pc = null;
    }

    if (useWebSocket) {
      this.signaling = new WebSocketSignaling();
    } else {
      this.signaling = new Signaling();
    }

    this.connectionId = uuid4();

    // Create peerConnection with proxy server and set up handlers
    this.pc = new Peer(this.connectionId, true);

    // Disconnect Event
    this.pc.addEventListener("disconnect", () => {
      _this.ondisconnect();
    });

    // Add Track Event
    this.pc.addEventListener("trackevent", (e) => {
      const data = e.detail;
      _this.replaceTrack(_this.localStream, data.track);
    });

    // Send Offer Event
    this.pc.addEventListener("sendoffer", (e) => {
      const offer = e.detail;
      _this.signaling.sendOffer(offer.connectionId, offer.sdp);
    });

    // Send Answer Event
    this.pc.addEventListener("sendanswer", (e) => {
      const answer = e.detail;
      _this.signaling.sendAnswer(answer.connectionId, answer.sdp);
    });

    // Send Candidate Event
    this.pc.addEventListener("sendcandidate", (e) => {
      const candidate = e.detail;
      _this.signaling.sendCandidate(
        candidate.connectionId,
        candidate.candidate,
        candidate.sdpMid,
        candidate.sdpMLineIndex,
      );
    });

    // Disconnect Event
    this.signaling.addEventListener("disconnect", async (e) => {
      const data = e.detail;
      if (_this.pc != null && _this.pc.connectionId == data.connectionId) {
        _this.ondisconnect();
      }
    });

    // Create data channel with proxy server and set up handlers
    this.channel = this.pc.createDataChannel(this.connectionId, "data");
    this.channel.onopen = function () {
      Logger.log("Datachannel connected.");
    };
    this.channel.onerror = function (e) {
      Logger.log(
        "The error " +
          e.error.message +
          " occurred\n while handling data with proxy server.",
      );
    };
    this.channel.onclose = function () {
      Logger.log("Datachannel disconnected.");
    };
    this.channel.onmessage = async (msg) => {
      // receive message from unity and operate message
      let data;
      // receive message data type is blob only on Firefox
      if (navigator.userAgent.indexOf("Firefox") != -1) {
        data = await msg.data.arrayBuffer();
      } else {
        data = msg.data;
      }
    };

    // Offer Response Handler Event
    this.signaling.addEventListener("offer", async (e) => {
      const offer = e.detail;
      const desc = new RTCSessionDescription({ sdp: offer.sdp, type: "offer" });
      if (_this.pc != null) {
        await _this.pc.onGotDescription(offer.connectionId, desc);
      }
    });

    // Answer Response Handler Event
    this.signaling.addEventListener("answer", async (e) => {
      const answer = e.detail;
      const desc = new RTCSessionDescription({
        sdp: answer.sdp,
        type: "answer",
      });
      if (_this.pc != null) {
        await _this.pc.onGotDescription(answer.connectionId, desc);
      }
    });

    // Candidate Response Handler Event
    this.signaling.addEventListener("candidate", async (e) => {
      const candidate = e.detail;
      const iceCandidate = new RTCIceCandidate({
        candidate: candidate.candidate,
        sdpMid: candidate.sdpMid,
        sdpMLineIndex: candidate.sdpMLineIndex,
      });
      if (_this.pc != null) {
        await _this.pc.onGotCandidate(candidate.connectionId, iceCandidate);
      }
    });

    // Resize Handler Event
    window.addEventListener(
      "resize",
      function () {
        _this.resizeVideo();
      },
      true,
    );

    // setup signaling
    await this.signaling.start();
  }

  resizeVideo() {
    const clientRect = this.video.getBoundingClientRect();
    const videoRatio = this.videoWidth / this.videoHeight;
    const clientRatio = clientRect.width / clientRect.height;

    this._videoScale =
      videoRatio > clientRatio
        ? clientRect.width / this.videoWidth
        : clientRect.height / this.videoHeight;
    const videoOffsetX =
      videoRatio > clientRatio
        ? 0
        : (clientRect.width - this.videoWidth * this._videoScale) * 0.5;
    const videoOffsetY =
      videoRatio > clientRatio
        ? (clientRect.height - this.videoHeight * this._videoScale) * 0.5
        : 0;
    this._videoOriginX = clientRect.left + videoOffsetX;
    this._videoOriginY = clientRect.top + videoOffsetY;
  }

  // replace video track related the MediaStream
  /*
    replaceTrack(stream, newTrack) {
        const tracks = stream.getVideoTracks();
        for (const track of tracks) {
			if(track.kind == 'video')
			{
				stream.removeTrack(track);
			}
        }

        stream.addTrack(newTrack);
		this.video.srcObject = stream;
    }

	replaceAudio(stream, newTrack) {
		const tracks = stream.getAudioTracks();
        for (const track of tracks) {
			if(track.kind == 'audio')
			{
				stream.removeTrack(track);
			}
        }

		stream.addTrack(newTrack);
		this.video.srcObject = stream;
	}
	*/

  replaceTrack(stream, newTrack) {
    if (newTrack.kind == "video") {
      const tracks = stream.getVideoTracks();
      for (const track of tracks) {
        if (track.kind == "video") {
          console.log("Removed video track");
          track.enabled = false;
          stream.removeTrack(track);
        }
      }
    } else if (newTrack.kind == "audio") {
      const tracks = stream.getAudioTracks();
      for (const track of tracks) {
        if (track.kind == "audio") {
          console.log("Removed audio track");
          track.enabled = false;
          stream.removeTrack(track);
        }
      }
    }

    if (newTrack.kind == "video") {
      console.log("Added video track");
    } else if (newTrack.kind == "audio") {
      console.log("Added audio track");
    }
    stream.addTrack(newTrack);
    this.video.srcObject = stream;
  }

  get videoWidth() {
    return this.video.videoWidth;
  }

  get videoHeight() {
    return this.video.videoHeight;
  }

  get videoOriginX() {
    return this._videoOriginX;
  }

  get videoOriginY() {
    return this._videoOriginY;
  }

  get videoScale() {
    return this._videoScale;
  }

  sendMsg(msg) {
    if (this.channel == null) {
      return;
    }
    switch (this.channel.readyState) {
      case "connecting":
        Logger.log("Connection not ready");
        break;
      case "open":
        this.channel.send(msg);
        break;
      case "closing":
        Logger.log("Attempt to sendMsg message while closing");
        break;
      case "closed":
        Logger.log("Attempt to sendMsg message while connection closed.");
        break;
    }
  }

  async stop() {
    if (this.signaling) {
      await this.signaling.stop();
      this.signaling = null;
    }

    if (this.pc) {
      this.pc.close();
      this.pc = null;
    }
  }
}
