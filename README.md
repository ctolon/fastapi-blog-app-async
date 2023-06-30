# FastAPI Async Project Template

## Proje için Gereksinimler

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).


## Backend yerel geliştirme (local development)

* Docker Compose ile servisleri başlatın:

```bash
docker-compose up -d
```

* Artık tarayıcınızı açabilir ve bu URL'lerle etkileşim kurabilirsiniz.:

Frontend için link: `http://localhost`

JSON - OpenAPI tabanlı Web REST API Backend için link: `http://localhost/api/`

Swagger UI ile otomatik etkileşimli dokümantasyon (OpenAPI backendinden): `http://localhost/docs`

ReDoc ile alternatif otomatik dokümantasyon (OpenAPI backendinden): `http://localhost/redoc`

PostgreSQL veri tabanı yönetmi için PGAdmin: `http://localhost:5050`

Celery worker yönetimi için Flower yönetim paneli `http://localhost:5555`

Traefik UI, yönlendirmelerin (routing) proxy tarafından nasıl işlendiğini görmek için: `http://localhost:8090`

**Note**: Geliştirme stack'inizi ilk başlattığınızda, hazır olması bir dakika sürebilir. Arka uç ise veritabanının hazır olmasını bekler ve her şeyi yapılandırır. İzlemek için logları kontrol edebilirsiniz..

Logları kontrol etmek için bu komut kullanılabilir:

```bash
docker-compose logs
```

Belirli bir servisin loglarını kontrol etmek için servisin adını ekleyin, ör.:

```bash
docker-compose logs backend
```

Docker'ınız `localhost`ta çalışmıyorsa (bu durumda yukarıdaki URL'ler çalışmaz), aşağıdaki **Docker Toolbox ile Geliştirme** ve **Özel IP ile Geliştirme** bölümlerine bakın..

## Backend yerel geliştirme, ekstra detaylar

### Genel akış

Bağımlılıklar varsayılan olarak `pip` paket yöneticisi ile yönetilir ve kurulur.

`./backend/src/` içinden tüm bağımlılıkları yükleyebilirsiniz.:

Ardından, editörünüzü `./backend/src/` konumunda açın (proje kökü: `./` yerine), böylece içinde kodunuzun bulunduğu bir `./src/` dizininde olacaksınız. Bu şekilde editörünüz tüm içe aktarmaları vb. bulabilecektir. Editörünüzün Pip ile az önce oluşturduğunuz ortamı kullandığından emin olun (Bunun için Conda, Virtual Environment ya da Docker Container'ı gibi çözümler uygulayabilirsiniz.).

`./backend/src/app/models/` içindeki SQLAlchemy modellerini, `./backend/app/app/schemas/` içindeki Pydantic şemalarını, `./backend/src/app/api/` içindeki API endpointlerini değiştirin veya ekleyin , CRUD (Oluştur, Oku, Güncelle, Sil) işlemler `./backend/src/app/crud/` içinde kullanılır ve tanımlanmıştır. En kolayı `post` için olanları (modeller, endpointler ve CRUD yardımcı programları) kopyalamak ve ihtiyaçlarınıza göre güncellemek olabilir.

Celery Worker'a görevler ekleyin ve değiştirin. `./backend/src/app/worker.py`.

Worker'a herhangi bir ek paket yüklemeniz gerekirse, onu bu dosyaya ekleyin: `./backend/Dockerfile.celeryworker`.

### Docker Compose Override

Geliştirme sırasında, yalnızca yerel geliştirme ortamını etkileyecek olan Docker Compose ayarlarını `docker-compose.override.yml` dosyasında değiştirebilirsiniz.

Bu dosyada yapılan değişiklikler yalnızca yerel geliştirme ortamını etkiler, production ortamını etkilemez. Böylece, geliştirme iş akışına yardımcı olan "geçici" değişiklikler ekleyebilirsiniz.

Örneğin, backend koduna sahip dizin, canlı olarak değiştirdiğiniz kodu kabın içindeki dizine eşleyen bir Docker "ana bilgisayar birimi" olarak bağlanır. Bu, Docker görüntüsünü yeniden oluşturmak zorunda kalmadan değişikliklerinizi hemen test etmenizi sağlar. Yalnızca geliştirme sırasında yapılmalıdır, production için Docker görüntüsünü backend kodunun en son sürümüyle oluşturmalısınız. Ancak geliştirme sırasında çok hızlı yineleme yapmanıza olanak tanır.

Varsayılan `/start.sh` web server başlatma scripti yerine `/start-reload.sh` çalıştıran bir komut geçersiz kılma da vardır. Tek bir sunucu işlemi başlatır (production için olduğu gibi birden çok yerine) ve kod değiştiğinde işlemi yeniden yükler. Bir syntax hatanız varsa ve Python dosyasını kaydederseniz, dosyanın bozulacağını ve containerın duracağını unutmayın. Bundan sonra, hatayı düzeltip tekrar çalıştırarak container'ı yeniden başlatabilirsiniz:

```console
$ docker-compose up -d
```

Ayrıca, yorum satırına alınmış bir `komut`" geçersiz kılma da vardır, bunun yorumunu kaldırabilir ve varsayılanı yorumlayabilirsiniz. backend containerının `hiçbir şey` yapmayan ancak containerı canlı tutan bir işlem yürütmesini sağlar. Bu, çalışan kapsayıcınızın içine girmenize ve örneğin yüklü bağımlılıkları test etmek için bir Python yorumlayıcısı gibi komutları yürütmenize veya değişiklikleri algıladığında yeniden yüklenen geliştirme sunucusunu başlatmanıza olanak tanır.

Bir `bash` session'ı ike containerın içine girmek için stacki şu şekilde başlatabilirsiniz::

```console
$ docker-compose up -d
```

Ve sonrasında `exec` komutu ile çalışan konteynırın içine girebilirsiniz:

```console
$ docker-compose exec blog-app-backend bash
```

Aşağıdaki gibi bir çıktı görmelisiniz:

```console
root@7f2607af31c3:/app#
```

bu, `/app` dizini altında bir `root` kullanıcısı olarak containerın içinde bir `bash` oturumunda olduğunuz anlamına gelir.

Orada hata ayıklama canlı yeniden yükleme sunucusunu çalıştırmak için `/start-reload.sh` scriptini kullanabilirsiniz. Bu komut dosyasını ile containerın içinden çalıştırabilirsiniz.

```console
$ bash /start-reload.sh
```

...Şöyle görünmeli:

```console
root@7f2607af31c3:/app# bash /start-reload.sh
```

ve ardından enter tuşuna basın. Bu, kod değişikliklerini algıladığında otomatik olarak yeniden yüklenen canlı yeniden yükleme sunucusunu çalıştırır..

Bununla birlikte, bir değişiklik değil, bir sözdizimi hatası algılarsa, bir hatayla duracaktır. Ancak container hala canlı olduğundan ve bir Bash oturumunda olduğunuzdan, hatayı düzelttikten sonra aynı komutu ("yukarı ok" ve "Enter") çalıştırarak hızla yeniden başlatabilirsiniz..

...Bu önceki ayrıntı, container hiçbir şey yapmadan canlı olmasını ve ardından bir Bash oturumunda onu canlı yeniden yükleme sunucusunu çalıştırmasını yararlı kılan şeydir.

### Backend tests

Backend testlerini çalıştırmak için şu komutu kullanın:

```console
$ DOMAIN=backend sh ./scripts/test.sh
```

`./scripts/test.sh` dosyası, bir test `docker-stack.yml` dosyası oluşturmak, stacki başlatmak ve test etmek için komutlara sahiptir.

Testler `pytest` tabanlıdır. Bu testleri güncelleyebilir ya da yeni testler ekleyebilirsiniz: `./backend/src/app/tests/`.

`GitLab CI` kullanıyorsanız testler otomatik olarak çalışır..

#### Local tests

Local testler bu komutla başlatılabilir:

```Bash
DOMAIN=backend sh ./scripts/test-local.sh
```
`./backend/src` dizini, docker containerının içinde bir "ana bilgisayar birimi" olarak bağlanır (`docker-compose.dev.volumes.yml` dosyasında ayarlanır).
Testi canlı kodda tekrar çalıştırabilirsiniz:

```Bash
docker-compose exec backend /app/tests-start.sh
```

#### Test running stack

Eğer containerlarınız ayaktaysa ve yalnızca testleri çalıştırmak istiyorsanız, şu komutu kullanabilirsiniz:

```bash
docker-compose exec backend /app/tests-start.sh
```

Bu `/app/tests-start.sh` scripti, containerların geri kalanının çalıştığından emin olduktan sonra `pytest`i çağırır. `pytest`'e fazladan argüman iletmeniz gerekirse, onları o komuta iletebilirsiniz ve iletileceklerdir.

Örneğin, testleri ilk hatada durdurmak için:

```bash
docker-compose exec backend bash /app/tests-start.sh -x
```

#### Test Coverage

Test scriptleri bağımsız değişkenleri `pytest`e ilettiğinden, `--cov-report=html` parametresi ileterek test kapsamı HTML raporu oluşturmayı etkinleştirebilirsiniz.

Kapsamlı HTML raporlarıyla yerel testleri çalıştırmak için::

```Bash
DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
```

Testleri, kapsam HTML raporları ile çalışan bir yığında çalıştırmak için:

```bash
docker-compose exec backend bash /app/tests-start.sh --cov-report=html
```

### Migrations

Yerel geliştirme sırasında `src` dizininiz container içinde bir volume olarak mount edildiğinden, migrationları container içinde `alembic` komutlarıyla da çalıştırabilirsiniz ve migration kodu (yalnızca container içinde olmak yerine) uygulama dizininizde olacaktır. Böylece onu git deponuza ekleyebilirsiniz.

Modellerinizin bir "revizyonunu" oluşturduğunuzdan ve veritabanınızı her değiştirdiğinizde bu revizyonla "yükselttiğinizden" emin olun. Bu, veritabanınızdaki tabloları güncelleyecek olan şeydir. Aksi halde uygulamanızda hatalar olacaktır!

* Backend container'nın içinde etkileşimli bir oturum başlatın:

```console
$ docker-compose exec blog-app-backend bash
```

* `./backend/src/app/models/` içinde yeni bir model oluşturduysanız, onu Python modülü olan `"./backend/app/app/db/base.py"` içine (`base.py`) aktardığınızdan (import ile) emin olun. aktarılan eden tüm modeller `alembic` tarafından kullanılacaktır.

* Bir modeli değiştirdikten sonra (örneğin, bir column ekleyerek), containerın içinde bir revizyon oluşturun, ör:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* `alembic` dizininde oluşturulan dosyaları `git` reposuna commit edin.

* Revizyonu oluşturduktan sonra, migrationı veritabanında çalıştırın (veritabanını gerçekten değiştirecek olan budur):

```console
$ alembic upgrade head
```

Migrationları hiç kullanmak istemiyorsanız, `./backend/src/app/db/init_db.py` dosyasındaki satırın yorumunu kaldırın:

```python
Base.metadata.create_all(bind=engine)
```

ve `prestart.sh` dosyasındaki aşağıda verilen bölümü yorum satırını alın:

```console
$ alembic upgrade head
```

Varsayılan modellerle başlamak istemiyor ve bunları kaldırmak / değiştirmek istiyorsanız, daha önce herhangi bir revizyon yapmadan en baştan, `./backend/src/alembic/versions/` altındaki revizyon dosyalarını (`.py` yani Python dosyalarını) kaldırabilirsiniz. Ardından, yukarıda açıklandığı gibi bir ilk migration oluşturun.

TODO komutu ve ve dene

### Development with Docker Toolbox

**Docker for Windows** veya **Docker for Mac** yerine Windows veya macOS'ta **Docker Toolbox** kullanıyorsanız, Docker bir VirtualBox Sanal Makinesinde çalışacak ve farklı bir yerel IP'ye sahip olacaktır (makinenizdeki `localhost` için IP adresi olan `127.0.0.1`).

Docker Toolbox sanal makinenizin adresi muhtemelen `192.168.99.100` olacaktır (varsayılan değer budur).

Bu yaygın bir durum olduğundan, `local.dockertoolbox.batuhan.com` etki alanı, yalnızca geliştirmeye yardımcı olmak için söz konusu (özel) IP'ye işaret eder (aslında `dockertoolbox.batuhan.com` ve tüm alt etki alanları bu IP'yi gösterir). Bu şekilde, yığını Docker Toolbox'ta başlatabilir ve bu etki alanını geliştirme için kullanabilirsiniz. Bu URL'yi Chrome'da açabileceksiniz ve yerel Docker Toolbox'ınızla sanki CORS (Çapraz Kaynak Paylaşımı) dahil bir bulut sunucusuymuş gibi doğrudan iletişim kuracak.

Projeyi oluştururken varsayılan CORS etkin etki alanlarını kullandıysanız, `local.dockertoolbox.batuhan.com` izin verilecek şekilde yapılandırıldı. Eklemediyseniz, onu `.env` dosyasındaki `BACKEND_CORS_ORIGINS` değişkenindeki listeye eklemeniz gerekecektir.

Bunu yığınınızda yapılandırmak için, `local.dockertoolbox.batuhan.com` etki alanını kullanarak aşağıdaki **change the development "domain"** bölümünü izleyin.

Bu adımları gerçekleştirdikten sonra `http://local.dockertoolbox.batuhan.com` adresini açabilmeniz gerekir ve bu, Docker Toolbox sanal makinenizde yığınınıza göre sunucu olacaktır.

Sondaki bölümde karşılık gelen tüm kullanılabilir URL'leri kontrol edin.

### Development in `localhost` with a custom domain

Etki alanı olarak `localhost`'tan farklı bir şey kullanmak isteyebilirsiniz. Örneğin, bir alt alan adı gerektiren tanımlama bilgileriyle ilgili sorun yaşıyorsanız ve Chrome, `localhost` kullanmanıza izin vermiyorsa vs.

Bu durumda, iki seçeneğiniz vardır: talimatları kullanarak sistem `hosts` dosyanızı aşağıdaki **Development with a custom IP** bölümündeki yönergelerle değiştirebilir veya yalnızca `localhost.batuhan.com`'u kullanabilirsiniz. `localhost` (IP `127.0.0.1`) ve tüm alt etki alanlarını gösterecek şekilde ayarlanmıştır. Ve gerçek bir etki alanı olduğu için, tarayıcılar geliştirme sırasında belirlediğiniz çerezleri vb. depolar.

Projeyi oluştururken varsayılan CORS etkin etki alanlarını kullandıysanız, `localhost.batuhan.com` izin verilecek şekilde yapılandırıldı. Eklemediyseniz, onu `.env` dosyasındaki `BACKEND_CORS_ORIGINS` değişkenindeki listeye eklemeniz gerekecektir.

Yığınınızda yapılandırmak için, `localhost.batuhan.com` etki alanını kullanarak aşağıdaki **Change the development "domain"** bölümünü izleyin.

Bu adımları gerçekleştirdikten sonra `http://localhost.batuhan.com` adresini açabilmeniz gerekir ve `localhost` içindeki yığınınıza göre sunucu olacaktır.

Sondaki bölümde karşılık gelen tüm kullanılabilir URL'leri kontrol edin.

### Development with a custom IP

Docker'ı `127.0.0.1` (`localhost`) ve `192.168.99.100`'den (Docker Toolbox'ın varsayılanı) farklı bir IP adresinde çalıştırıyorsanız, bazı ek adımlar gerçekleştirmeniz gerekecektir. Özel bir Sanal Makine, ikincil bir Docker Toolbox çalıştırıyorsanız veya Docker'ınız ağınızdaki farklı bir makinede bulunuyorsa durum böyle olacaktır.

Bu durumda, sahte bir yerel etki alanı (`dev.blog-app`) kullanmanız ve bilgisayarınızın etki alanına özel IP tarafından hizmet verildiğini düşünmesini sağlamanız gerekir (ör. `192.168.99.150`).

Varsayılan CORS özellikli etki alanlarını kullandıysanız, `dev.blog-app` izin verilecek şekilde yapılandırıldı. Özel bir tane istiyorsanız, onu `.env` dosyasındaki `BACKEND_CORS_ORIGINS` değişkenindeki listeye eklemeniz gerekir.

* Bir metin düzenleyici kullanarak "hosts" dosyanızı yönetici yetkisiyle açın:
  * **Windows için Not**: Windows'taysanız, ana Windows menüsünü açın, `notepad`i arayın, sağ tıklayın ve "Yönetici olarak aç" seçeneğini veya benzerini seçin. Ardından `Dosya` menüsüne tıklayın, `Dosya aç`, `c:\Windows\System32\Drivers\etc\` dizinine gidin, yalnızca `Metin (.txt) dosyaları` yerine "Tüm dosyalar"ı gösterme seçeneğini seçin ve `hosts` dosyasını açın.
  * **Mac ve Linux için not**: "hosts" dosyanız muhtemelen `/etc/hosts` konumundadır, onu `sudo nano /etc/hosts` çalıştıran bir terminalde düzenleyebilirsiniz.

* Sahip olabileceği içeriğe ek olarak, özel IP (ör. `192.168.99.150`) bir boşluk karakteri ve sahte yerel alan adınız olan `dev.blog-app` ile yeni bir satır ekleyin.

Yeni satır şöyle görünebilir:

```
192.168.99.100    dev.blog-app
```

* Dosyayı kaydedin.
  * **Windows için not**: Dosyayı `.txt` uzantısı olmadan `Tüm dosyalar` olarak kaydettiğinizden emin olun. Varsayılan olarak, Windows uzantıyı eklemeye çalışır. Dosyanın olduğu gibi, uzantısız olarak kaydedildiğinden emin olun

...bu, bilgisayarınızın sahte yerel etki alanına o özel IP tarafından hizmet verildiğini düşünmesine neden olacak ve bu URL'yi tarayıcınızda açtığınızda, `dev.blog-app'a gitmesi istendiğinde yerel olarak çalışan sunucunuzla doğrudan konuşacaktır` ve aslında bilgisayarınızda çalışırken bunun bir uzak sunucu olduğunu düşünün.

Yığınınızda yapılandırmak için, `dev.blog-app` alanını kullanarak aşağıdaki **Change the development "domain"*** bölümünü izleyin.

Bu adımları gerçekleştirdikten sonra `http://dev.blog-app` adresini açabilmeniz gerekir ve bu `localhost` içindeki yığınınız tarafından sunucu olacaktır.

Sondaki bölümde karşılık gelen tüm kullanılabilir URL'leri kontrol edin.

### Change the development "domain"

Yerel yığınınızı `localhost`'tan farklı bir etki alanı ile kullanmanız gerekiyorsa, kullandığınız etki alanının yığınınızın kurulduğu IP'yi işaret ettiğinden emin olmanız gerekir. Yukarıdaki bölümlerde bunu başarmanın farklı yollarını görün (ör. `local.dockertoolbox.batuhan.com` ile Docker Toolbox'ı kullanmak, `localhost.batuhan.com`u kullanmak veya `dev.blog-app`'i kullanmak).

Örneğin, Docker Compose kurulumunuzu basitleştirmek ve API belgelerinin (Swagger UI) API'nizin nerede olduğunu bilmesini sağlamak için, geliştirme için o etki alanını kullandığınızı bilmesini sağlamalısınız. 2 dosyada 1 satırı düzenlemeniz gerekecek.

* `./.env` konumunda bulunan dosyayı açın. Şunun gibi bir satırı düzenleyin:

```
DOMAIN=localhost
```

* Kullanacağınız etki alanıyla değiştirin, örn.:

```
DOMAIN=localhost.batuhan.com
```

Bu değişken, Docker Compose dosyaları tarafından kullanılacaktır.

* Şimdi `./frontend/.env` konumunda bulunan dosyayı açın. Şunun gibi bir satırı düzenleyin:

```
VUE_APP_DOMAIN_DEV=localhost
```

* Kullanacağınız etki alanıyla değiştirin, örn.:

```
VUE_APP_DOMAIN_DEV=localhost.batuhan.com
```

Bu değişken, diğer `VUE_APP_ENV` değişkeni `development` olarak ayarlandığında, backend API'nizle etkileşim kurarken frontedin o etki alanı ile iletişim kurmasını sağlar.

Bu iki satırı değiştirdikten sonra yığınınızı yeniden başlatabilirsiniz.:

```bash
docker-compose up -d
```

ve sondaki bölümde karşılık gelen tüm kullanılabilir URL'leri kontrol edin.

## Deployment

You can deploy the stack to a Docker Swarm mode cluster with a main Traefik proxy, set up using the ideas from <a href="https://dockerswarm.rocks" target="_blank">DockerSwarm.rocks</a>, to get automatic HTTPS certificates, etc.

Ve bunu otomatik olarak yapmak için CI (sürekli entegrasyon) sistemlerini kullanabilirsiniz..

Ama önce birkaç şeyi yapılandırmanız gerekiyor.

### Traefik network

Bu yığın, genel Traefik ağının tıpkı <a href="https://dockerswarm.rocks" class="external-link" target="_blank">DockerSwarm.rocks</a> DockerSwarm'daki öğreticilerde olduğu gibi "traefik-public" olarak adlandırılmasını bekler.

Farklı bir Traefik genel ağ adı kullanmanız gerekiyorsa, bunu `docker-compose.yml` dosyaları bölümünde güncelleyin.:

```YAML
networks:
  traefik-public:
    external: true
```

`traefik-public`'i kullanılan Traefik ağının adıyla değiştirin. Ardından onu `.env` dosyasında güncelleyin:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```

### Persisting Docker named volumes

Bir birim kullanan her hizmetin (Docker kapsayıcısı), verileri koruyabilmesi için her zaman kümedeki aynı Docker "düğümüne" dağıtıldığından emin olmanız gerekir. Aksi takdirde, her seferinde farklı bir düğüme konuşlandırılabilir ve her seferinde hizmet başlatılmadan önce bu yeni düğümde birim oluşturulur. Sonuç olarak, hizmetiniz her seferinde sıfırdan başlıyor ve önceki tüm verileri kaybediyormuş gibi görünür.

Bu, veritabanı çalıştıran bir hizmet için özellikle önemlidir. Ancak, dosyaları ana backend hizmetinizde kaydediyorsanız (örneğin, bu dosyalar kullanıcılarınız tarafından yüklendiyse veya sisteminiz tarafından oluşturulduysa) aynı sorun geçerli olacaktır.

Bunu çözmek için, belirli bir etikete sahip bir Docker düğümüne dağıtılmalarını sağlamak için bir veya daha fazla veri birimi (veritabanları gibi) kullanan hizmetlere kısıtlamalar koyabilirsiniz. Ve elbette, bu etiketin düğümlerinizden birine (yalnızca birine) atanması gerekir..

#### Adding services with volumes

Bir birim kullanan her hizmet için (veritabanları, karşıya yüklenen dosyalara sahip hizmetler, vb.) `docker-compose.yml` dosyanızda bir etiket kısıtlaması olmalıdır.

Etiketlerinizin yığın başına birim başına benzersiz olduğundan emin olmak için (örneğin, `prod` ve `stag` için aynı olmadıklarından) yığınınızın adını prefix olarak eklemelisiniz ve ardından aynı birim adını kullanmalısınız.

Ardından, `constraints` bölümlerinde düzeltilmesi gereken hizmetler için bu kısıtlamaları `docker-compose.yml` dosyanızda bulundurmanız gerekir.

`prod` ve `stag` gibi farklı ortamları kullanabilmek için, yığının adını ortam değişkeni olarak iletmelisiniz. Şunun gibi:

```bash
STACK_NAME=stag-blog-app sh ./scripts/deploy.sh
```

Bu ortam değişkenini `docker-compose.yml` dosyaları içinde kullanmak ve genişletmek için aşağıdaki gibi hizmetlere kısıtlamalar ekleyebilirsiniz:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.${STACK_NAME?Variable not set}.app-db-data == true
```

`${STACK_NAME?Variable not set}` kısmına dikkat edin. `./scripts/deploy.sh` komut dosyasında `docker-compose.yml` dönüştürülür ve şunu içeren bir "docker-stack.yml" dosyasına kaydedilir.


```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.blog-app.app-db-data == true
```

**Not**: `${STACK_NAME?Variable not set`, "`STACK_NAME` ortam değişkenini kullanın, ancak bir değer atanmadıysa, `Variable not set` hatası gösterin" anlamına gelir.

Yığınınıza daha fazla birim eklerseniz, o adlandırılmış birimi kullanan hizmetlere karşılık gelen kısıtlamaları eklediğinizden emin olmanız gerekir.

Ardından, bu etiketleri Docker Swarm modu kümenizdeki bazı düğümlerde oluşturmanız gerekir. Otomatik olarak yapmak için `docker-auto-labels` kullanabilirsiniz.

#### `docker-auto-labels`

Docker yığınınızdaki (Docker Compose dosyası) yerleşim kısıtlaması etiketlerini otomatik olarak okumak ve bu etiketler henüz mevcut değilse, bunları Swarm modu kümenizdeki rastgele bir Docker düğümüne atamak için [`docker-auto-labels`](https://github.com/batuhan/docker-auto-labels) kullanabilirsiniz.

Bunu yapmak için `docker-auto-labels` yükleyebilirsiniz:

```bash
pip install docker-auto-labels
```

Ardından, `docker-stack.yml` dosyanızı parametre olarak geçirerek çalıştırın:

```bash
docker-auto-labels docker-stack.yml
```

Gerekli etiketler zaten mevcutsa hiçbir şeyi değiştirmediğinden, bu komutu her deploy için, deploy yapmadan hemen önce çalıştırabilirsiniz.

#### (Optionally) adding labels manually

`docker-auto-labels` kullanmak istemiyorsanız veya herhangi bir nedenle kısıtlama etiketlerini Docker Swarm modu kümenizdeki belirli düğümlere manuel olarak atamak istiyorsanız, aşağıdakileri yapabilirsiniz:

* İlk olarak, SSH aracılığıyla Docker Swarm mod kümenize bağlanın.

* Ardından, mevcut düğümleri ile kontrol edin:

```console
$ docker node ls


// you would see an output like:

ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
nfa3d4df2df34as2fd34230rm *   dog.example.com        Ready               Active              Reachable
2c2sd2342asdfasd42342304e     cat.example.com        Ready               Active              Leader
c4sdf2342asdfasd4234234ii     snake.example.com      Ready               Active              Reachable
```

ardından listeden bir düğüm seçin. Örneğin, `dog.example.com`.

* Etiketi bu düğüme ekleyin. Etiket olarak dağıtmakta olduğunuz yığının adını, ardından bir nokta (`.`) ve ardından adlandırılmış birimi kullanın ve değer olarak yalnızca `true`, örn.:

```bash
docker node update --label-add blog-app.app-db-data=true dog.example.com
```

* To zaman sahip olduğunuz her yığın sürümü için aynısını yapmanız gerekir. Örneğin, stag aşaması için şunları yapabilirsiniz:

```bash
docker node update --label-add stag-blog-app.app-db-data=true cat.example.com
```

### Deploy to a Docker Swarm mode cluster

There are 3 steps:

1. Uygulama imagelarını **Build** etme
2. Opsiyonel olarak, özelleştirilmiş imagelarınızı Docker Registry'e **push** etmek.
3. Yığını **Deploy** etmek

---

İşte ayrıntılı adımlar:

1. **Uygulama imagelarını Build etme**

* Bir sonraki komuttan hemen önce bu ortam değişkenlerini ayarlayın:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Sağlanan `scripts/build.sh` dosyasını bu ortam değişkenleriyle birlikte kullanın:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build.sh
```

2. **Opsiyonel olarak, özelleştirilmiş imagelarınızı Docker Registry'e push etmek**

**Not**: Docker Swarm modu "kümesi" dağıtımında birden fazla sunucu varsa, görüntüleri bir registry'e göndermeniz veya görüntüleri her sunucuda oluşturmanız gerekir; böylece kümenizdeki sunucuların her biri kapsayıcıları başlatmaya çalıştığında, Docker görüntülerini onlar için bir Docker Registry'den çekerek veya zaten yerel olarak oluşturmuş olduğu için çekebilir.

Bir registry kullanıyorsanız ve imagelarınızı aktarıyorsanız, önceki komut dosyasını çalıştırmayı atlayabilir ve bunun yerine tek seferde bunu kullanabilirsiniz.

* Bu ortam değişkenlerini ayarlayın:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Sağlanan `scripts/build-push.sh` dosyasını bu ortam değişkenleriyle kullanın:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build-push.sh
```

3. **Deploy your stack**

* Bu ortam değişkenlerini ayarlayın:
  * `DOMAIN=blog-app`
  * `TRAEFIK_TAG=blog-app`
  * `STACK_NAME=blog-app`
  * `TAG=prod`
* Sağlanan `scripts/deploy.sh` dosyasını bu ortam değişkenleriyle kullanın:

```bash
DOMAIN=blog-app \
TRAEFIK_TAG=blog-app \
STACK_NAME=blog-app \
TAG=prod \
bash ./scripts/deploy.sh
```

---

Fikrinizi değiştirirseniz ve örneğin her şeyi farklı bir etki alanına deploy etmek isterseniz, önceki komutlarda yalnızca `DOMAIN` ortam değişkenini değiştirmeniz gerekir. Yığınınızın `preproduction` gibi farklı bir sürümünü/ortamını eklemek isterseniz, yalnızca komutunuzda `TAG=preproduction` ayarını yapmanız ve bu diğer ortam değişkenlerini buna göre güncellemeniz gerekir. Aynı kümede aynı uygulamanın farklı ortamlarına ve dağıtımlarına sahip olabilmeniz için her şey işe yarayacaktır.

#### Deployment Technical Details

Build etme ve pushlama, `docker-compose` komutu kullanılarak `docker-compose.yml` dosyasıyla yapılır. `docker-compose.yml` dosyası, varsayılan ortam değişkenleriyle `.env` dosyasını kullanır. Komut dosyaları bazı ek ortam değişkenlerini de ayarlar.

Deployment, `docker-swarm` yerine `docker stack` kullanılmasını gerektirir ve ortam değişkenlerini veya `.env` dosyalarını okuyamaz. Bu nedenle, `deploy.sh` scripti, `docker-compose.yml`den gelen yapılandırmalarla ve ortam değişkenlerini buna enjekte ederek bir `docker-stack.yml` dosyası oluşturur. Ve sonra yığını dağıtmak için kullanır.

İsterseniz, aynı komut dosyalarına dayanarak işlemi manuel olarak el ile yapabilirsiniz. Genel yapı şu şekildedir:

```bash
# Use the environment variables passed to this script, as TAG and FRONTEND_ENV
# And re-create those variables as environment variables for the next command
TAG=${TAG?Variable not set} \
# Set the environment variable FRONTEND_ENV to the same value passed to this script with
# a default value of "production" if nothing else was passed
FRONTEND_ENV=${FRONTEND_ENV-production?Variable not set} \
# The actual comand that does the work: docker-compose
docker-compose \
# Pass the file that should be used, setting explicitly docker-compose.yml avoids the
# default of also using docker-compose.override.yml
-f docker-compose.yml \
# Use the docker-compose sub command named "config", it just uses the docker-compose.yml
# file passed to it and prints their combined contents
# Put those contents in a file "docker-stack.yml", with ">"
config > docker-stack.yml

# The previous only generated a docker-stack.yml file,
# but didn't do anything with it yet

# docker-auto-labels makes sure the labels used for constraints exist in the cluster
docker-auto-labels docker-stack.yml

# Now this command uses that same file to deploy it
docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"
```

### Continuous Integration / Continuous Delivery

GitLab CI kullanıyorsanız, `.gitlab-ci.yml` dosyası bu sürecin deploymentını otomatize edebilir. GitLab yapılandırmalarınıza göre güncellemeniz gerekebilir.

Başka bir CI/CD sağlayıcısı kullanıyorsanız, tüm gerçek betik adımları kolayca yeniden kullanabileceğiniz `bash` scriptlerinde gerçekleştirildiğinden, dağıtımınızı bu `.gitlab-ci.yml` dosyasından temel alabilirsiniz.

GitLab CI, GitLab akışını izleyen 2 ortam varsayılarak yapılandırılır:

* `production` branchinden `prod` (production)
* `master` branchinden `stag` (staging).

Örneğin, daha fazla ortam eklemeniz gerekirse, client tarafından onaylanan bir `preprod` branchi kullanmayı hayal edebilirsiniz, `.gitlab-ci.yml` içindeki `stag` için yapılandırmaları kopyalayabilir ve ilgili değişkenleri yeniden adlandırabilirsiniz. Docker Compose dosyası ve ortam değişkenleri, ihtiyacınız olduğu kadar çok ortamı destekleyecek şekilde yapılandırılmıştır, böylece yalnızca `.gitlab-ci.yml` (veya kullandığınız CI sistemi yapılandırması) üzerinde değişiklik yapmanız yeterlidir.

## Docker Compose files and env vars

Tüm yığına uygulanan tüm yapılandırmaları içeren bir ana `docker-compose.yml` dosyası vardır ve `docker-compose` tarafından otomatik olarak kullanılır.

Ayrıca, geliştirme için override özelliğine sahip bir `docker-compose.override.yml` de vardır, örneğin kaynak kodunu bir volume olarak bağlamak için. `docker-compose.yml` üzerinde override uygulamak için `docker-compose` tarafından otomatik olarak kullanılır.

Bu Docker Compose dosyaları, containerlara ortam değişkenleri olarak enjekte edilecek yapılandırmaları içeren `.env` dosyasını kullanır.

Ayrıca, `docker-compose` komutunu çağırmadan önce scriptlerde ayarlanan ortam değişkenlerinden alınan bazı ek yapılandırmaları kullanırlar.

Tamamı, geliştirme, oluşturma, test etme ve devreye alma gibi birkaç `aşamayı` desteklemek üzere tasarlanmıştır. Ayrıca, hazırlama ve üretim gibi farklı ortamlara konuşlandırmaya izin verir (ve çok kolay bir şekilde daha fazla ortam ekleyebilirsiniz).

Minimum kod ve konfigürasyon tekrarına sahip olacak şekilde tasarlanmıştır, böylece bir şeyi değiştirmeniz gerekirse, onu minimum sayıda yerde değiştirmeniz gerekir. Bu nedenle dosyalar, otomatik olarak genişleyen ortam değişkenlerini kullanır. Bu şekilde, örneğin farklı bir etki alanı kullanmak istiyorsanız, etki alanını Docker Compose dosyaları içinde birkaç yerde değiştirmek zorunda kalmak yerine, `docker-compose` komutunu farklı bir `DOMAIN` ortam değişkeniyle çağırabilirsiniz.

Ayrıca, `preprod` gibi başka bir deployment ortamına sahip olmak istiyorsanız, ortam değişkenlerini değiştirmeniz yeterlidir, ancak aynı Docker Compose dosyalarını kullanmaya devam edebilirsiniz.

### The .env file

`.env` dosyası, tüm yapılandırmalarınızı, oluşturulan anahtarları ve parolaları vb. içeren dosyadır.

İş akışınıza bağlı olarak, örneğin projeniz herkese açıksa, onu Git'ten hariç tutmak isteyebilirsiniz. Bu durumda, projenizi oluştururken veya dağıtırken CI araçlarınızın bunu elde etmesi için bir yol oluşturduğunuzdan emin olmanız gerekir.

Bunu yapmanın bir yolu, her bir ortam değişkenini CI/CD sisteminize eklemek ve `.env` dosyasını okumak yerine `docker-compose.yml` dosyasını o belirli env değişkenini okuyacak şekilde güncellemek olabilir..

## URL Listesi

Bunlar, proje tarafından kullanılacak ve oluşturulacak URL'lerdir.

### Production URLs

Production URLs, from the branch `production`.

Frontend: `https://blog-app`

Backend: `https://blog-app/api/`

Otomatik Etkileşimli Doküman (Swagger UI): `https://blog-app/docs`

Otomatik Etkileşimli Doküman (ReDoc): `https://blog-app/redoc`

PGAdmin: `https://pgadmin.blog-app`

Flower: `https://flower.blog-app`

### Staging URLs

Staging URLs, from the branch `master`.

Frontend: `https://stag.blog-app`

Backend: `https://stag.blog-app/api/`

Otomatik Etkileşimli Doküman (Swagger UI): `https://stag.blog-app/docs`

Otomatik Etkileşimli Doküman (ReDoc): `https://stag.blog-app/redoc`

PGAdmin: `https://pgadmin.stag.blog-app`

Flower: `https://flower.stag.blog-app`

### Geliştirme URL'leri

Yerel geliştirme için geliştirme URL'leri.

Frontend: `http://localhost`

Backend: `http://localhost/api/`

Otomatik Etkileşimli Doküman (Swagger UI): `https://localhost/docs`

Otomatik Etkileşimli Doküman (ReDoc): `https://localhost/redoc`

PGAdmin: `http://localhost:5050`

Flower: `http://localhost:5555`

Traefik UI: `http://localhost:8090`

### Docker Toolbox URL'leri ile Geliştirme

Yerel geliştirme için geliştirme URL'leri.

Frontend: `http://local.dockertoolbox.batuhan.com`

Backend: `http://local.dockertoolbox.batuhan.com/api/`

Otomatik Etkileşimli Doküman (Swagger UI): `https://local.dockertoolbox.batuhan.com/docs`

Otomatik Etkileşimli Doküman (ReDoc): `https://local.dockertoolbox.batuhan.com/redoc`

PGAdmin: `http://local.dockertoolbox.batuhan.com:5050`

Flower: `http://local.dockertoolbox.batuhan.com:5555`

Traefik UI: `http://local.dockertoolbox.batuhan.com:8090`

### Özel IP URL'leri ile geliştirme

Yerel geliştirme için geliştirme URL'leri.

Frontend: `http://dev.blog-app`

Backend: `http://dev.blog-app/api/`

Otomatik Etkileşimli Doküman (Swagger UI): `https://dev.blog-app/docs`

Otomatik Etkileşimli Doküman (ReDoc): `https://dev.blog-app/redoc`

PGAdmin: `http://dev.blog-app:5050`

Flower: `http://dev.blog-app:5555`

Traefik UI: `http://dev.blog-app:8090`

### Özel domain URL'leri ile localhost'ta geliştirme

Yerel geliştirme için geliştirme URL'leri listesi.

Frontend: `http://localhost.batuhan.com`

Backend: `http://localhost.batuhan.com/api/`

Otomatik Etkileşimli Doküman (Swagger UI): `https://localhost.batuhan.com/docs`

Otomatik Etkileşimli Doküman (ReDoc): `https://localhost.batuhan.com/redoc`

PGAdmin: `http://localhost.batuhan.com:5050`

Flower: `http://localhost.batuhan.com:5555`

Traefik UI: `http://localhost.batuhan.com:8090`
