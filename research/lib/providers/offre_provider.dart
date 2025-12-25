import 'package:flutter/foundation.dart';
import '../models/offre.dart';
import '../services/offre_service.dart';

class OffreProvider with ChangeNotifier {
  final OffreService _offreService = OffreService();
  List<Offre> _offres = [];
  bool _isLoading = false;
  String? _error;

  List<Offre> get offres => _offres;
  bool get isLoading => _isLoading;
  String? get error => _error;

  Future<void> loadOffres({
    String? type,
    String? lieu,
    String? search,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _offres = await _offreService.getOffres(
        type: type,
        lieu: lieu,
        search: search,
      );
      _error = null;
    } catch (e) {
      _error = e.toString();
    }

    _isLoading = false;
    notifyListeners();
  }

  Future<void> refreshOffres() async {
    await loadOffres();
  }
}

