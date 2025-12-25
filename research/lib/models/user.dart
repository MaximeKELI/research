class User {
  final int id;
  final String email;
  final String role;
  final String? photoUrl;
  final DateTime createdAt;

  User({
    required this.id,
    required this.email,
    required this.role,
    this.photoUrl,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      email: json['email'],
      role: json['role'],
      photoUrl: json['photo_url'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'role': role,
      'photo_url': photoUrl,
      'created_at': createdAt.toIso8601String(),
    };
  }
}



