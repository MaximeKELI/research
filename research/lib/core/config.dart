class ApiConfig {
  // Modifier cette URL selon votre configuration
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator
  // static const String baseUrl = 'http://localhost:8000'; // iOS simulator
  // static const String baseUrl = 'http://192.168.1.X:8000'; // Device physique
  
  static const String apiPrefix = '/api';
  
  static String get apiUrl => '$baseUrl$apiPrefix';
}

class AppConfig {
  static const String appName = 'JobApp';
  static const String appVersion = '1.0.0';
}

