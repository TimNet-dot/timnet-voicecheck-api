dependencies:
  flutter_sound: ^9.2.13
FlutterSoundRecorder _recorder;

void startStream() async {
  await _recorder.openAudioSession();
  await _recorder.startRecorder(toStream: (buffer) {
    sendAudioFrame(buffer); // Frame direkt zur API senden
  });
}
void sendAudioFrame(Uint8List buffer) async {
  final response = await http.post(
    Uri.parse('https://timnet-voicecheck-api.onrender.com/live'),
    headers: {'Content-Type': 'application/octet-stream'},
    body: buffer,
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    setState(() {
      tone = data['tone'];
      pitchLabel = data['pitch'];
      speechSpeed = data['speed'];
      toneConfidence = data['confidence'];
      pitchData = generatePitchSpots(data['pitch_curve']);
    });
  }
}
@app.post("/live")
async def analyze_live_audio(request: Request):
    raw_audio = await request.body()
    result = analyze_audio_frame(raw_audio)  # deine Analysefunktion
    return JSONResponse(content=result)
Timer.periodic(Duration(seconds: 2), (timer) {
  final buffer = getAudioFrame(); // abgreifen
  sendAudioFrame(buffer);         // ab zur API
});
