# Ứng Dụng Flask với Demo Xác Thực Không Mã

Một ứng dụng Flask đơn giản thể hiện xác thực không mã nguồn, trong đó bộ cân bằng tải xử lý quá trình xác thực.

Chi tiết triển khai: https://dev.to/hoangquochung1110/deploy-oidc-authentication-on-aws-with-no-coding-using-aws-cognito-and-application-load-balancer-1g8o

Để biết hướng dẫn cài đặt, vui lòng xem [INSTALL.md](INSTALL.md).

## Tính Năng

- Xác thực không mã - quá trình xác thực được xử lý bởi bộ cân bằng tải
- Không cần triển khai máy khách (client) OIDC trong mã ứng dụng
- Hiển thị hồ sơ người dùng với thông tin được truyền từ bộ cân bằng tải
- Kiến trúc ứng dụng đơn giản hóa tập trung vào logic nghiệp vụ

## Cấu Trúc Dự Án

Dự án có cấu trúc đơn giản không có mã xác thực trong chính ứng dụng:

```
.
├── app.py              # Ứng dụng Flask chính
├── templates/          # Các mẫu HTML
│   ├── index.html      # Trang chủ
│   └── profile.html    # Trang hồ sơ người dùng
└── .env                # Cấu hình môi trường
```

## Cách Thức Hoạt Động

Trong demo này:

1. Bộ cân bằng tải đóng vai trò là dịch vụ xác thực
2. Khi người dùng truy cập tài nguyên được bảo vệ, bộ cân bằng tải:
   - Chặn yêu cầu
   - Chuyển hướng đến nhà cung cấp xác thực nếu cần
   - Xử lý tất cả các luồng OIDC/xác thực
   - Truyền thông tin người dùng đến ứng dụng

3. Ứng dụng chỉ tập trung vào chức năng cốt lõi của nó, không có mã xác thực

## Lợi Ích của Xác Thực Không Mã

- **Mã Ứng Dụng Đơn Giản Hóa**: Không cần triển khai và duy trì mã xác thực
- **Bảo Mật Tập Trung**: Xác thực được quản lý ở cấp cơ sở hạ tầng
- **Giảm Phụ Thuộc**: Không cần thư viện xác thực trong ứng dụng
- **Bảo Mật Nhất Quán**: Xác thực đồng nhất trên nhiều ứng dụng
- **Bảo Trì Dễ Dàng Hơn**: Cập nhật xác thực diễn ra ở cấp bộ cân bằng tải

## Cấu Hình

Vì xác thực được xử lý bởi bộ cân bằng tải, nên chỉ cần cấu hình tối thiểu trong chính ứng dụng. 